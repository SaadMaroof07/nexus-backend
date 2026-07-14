import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CallConsumer(AsyncWebsocketConsumer):
    """
    Relays WebRTC signaling messages (offer, answer, ICE candidates)
    between exactly two peers in the same room. Never echoes a
    message back to the sender that sent it.
    """

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'call_{self.room_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Tell the OTHER peer (not myself) that someone joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'peer_joined',
                'sender_channel': self.channel_name,
                'room_id': self.room_id,
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'relay_message',
                'message': {'event': 'user_left'},
                'sender_channel': self.channel_name,
            }
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'relay_message',
                'message': data,
                'sender_channel': self.channel_name,
            }
        )

    async def peer_joined(self, event):
        if event.get('sender_channel') == self.channel_name:
            return
        await self.send(text_data=json.dumps({'event': 'user_joined', 'room_id': event.get('room_id')}))

    async def relay_message(self, event):
        # IMPORTANT: never send a message back to the same client that sent it
        if event.get('sender_channel') == self.channel_name:
            return
        await self.send(text_data=json.dumps(event['message']))