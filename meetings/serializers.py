from rest_framework import serializers
from django.utils import timezone
from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    participant_name = serializers.CharField(source='participant.username', read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'organizer', 'organizer_name', 'participant', 'participant_name',
            'title', 'description', 'start_time', 'end_time', 'status',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'organizer', 'status', 'created_at', 'updated_at')

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')

        # Basic sanity checks
        if start and end and start >= end:
            raise serializers.ValidationError("End time must be after start time.")

        if start and start < timezone.now():
            raise serializers.ValidationError("Cannot schedule a meeting in the past.")

        # ---------- Conflict detection ----------
        request = self.context.get('request')
        participant = data.get('participant')

        if request and participant and start and end:
            organizer = request.user

            # Check if EITHER person already has an overlapping accepted/pending meeting
            overlapping = Meeting.objects.filter(
                status__in=['pending', 'accepted'],
                start_time__lt=end,
                end_time__gt=start,
            ).filter(
                models_q_organizer_or_participant(organizer, participant)
            )

            if overlapping.exists():
                raise serializers.ValidationError(
                    "This time slot conflicts with an existing meeting for you or the participant."
                )

        return data


def models_q_organizer_or_participant(organizer, participant):
    from django.db.models import Q
    return (
        Q(organizer=organizer) | Q(participant=organizer) |
        Q(organizer=participant) | Q(participant=participant)
    )