import re

from django.test import SimpleTestCase

from . import routing as calls_routing


class CallRoutingTests(SimpleTestCase):
    def test_room_id_regex_allows_hyphenated_values(self):
        pattern = calls_routing.websocket_urlpatterns[0].pattern.regex
        self.assertTrue(re.match(pattern, 'ws/call/meeting-123/'))
