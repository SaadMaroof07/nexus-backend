from rest_framework import permissions


class IsOrganizerOrParticipant(permissions.BasePermission):
    """
    Only the two people involved in a meeting (organizer or participant)
    are allowed to view, accept, reject, or cancel it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.organizer or request.user == obj.participant