import logging

from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Meeting
from .serializers import MeetingSerializer
from .permissions import IsOrganizerOrParticipant

logger = logging.getLogger(__name__)


class MeetingViewSet(viewsets.ModelViewSet):
 
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
       
        user = self.request.user
        return (
            Meeting.objects
            .filter(Q(organizer=user) | Q(participant=user))
            .select_related('organizer', 'participant')
        )

    def get_permissions(self):
        if self.action in ('retrieve', 'accept', 'reject', 'destroy'):
            return [permissions.IsAuthenticated(), IsOrganizerOrParticipant()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        meeting = serializer.save(organizer=self.request.user)
        logger.info(
            "Meeting scheduled: '%s' | organizer=%s | participant=%s | %s -> %s",
            meeting.title, meeting.organizer, meeting.participant,
            meeting.start_time, meeting.end_time,
        )

    def perform_destroy(self, instance):
        if self.request.user != instance.organizer:
            raise PermissionDenied("Only the organizer can cancel this meeting.")
        logger.info("Meeting cancelled: '%s' (id=%s)", instance.title, instance.id)
        instance.delete()


    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
      
        meeting = self.get_object()

        if request.user != meeting.participant:
            return Response(
                {'error': 'Only the invited participant can accept this meeting.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        meeting.status = 'accepted'
        meeting.save(update_fields=['status', 'updated_at'])
        logger.info("Meeting accepted: '%s' (id=%s)", meeting.title, meeting.id)

        return Response(MeetingSerializer(meeting).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        
        meeting = self.get_object()

        if request.user != meeting.participant:
            return Response(
                {'error': 'Only the invited participant can reject this meeting.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        meeting.status = 'rejected'
        meeting.save(update_fields=['status', 'updated_at'])
        logger.info("Meeting rejected: '%s' (id=%s)", meeting.title, meeting.id)

        return Response(MeetingSerializer(meeting).data, status=status.HTTP_200_OK)
