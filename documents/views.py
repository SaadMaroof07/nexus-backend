from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):


    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # For now: user sees documents they uploaded.
        # (Sharing with meeting participants can be layered on later.)
        return Document.objects.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def perform_destroy(self, instance):
        if instance.uploaded_by != self.request.user:
            return Response(
                {'error': 'Only the uploader can delete this document.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=True, methods=['patch'], parser_classes=[MultiPartParser, FormParser])
    def sign(self, request, pk=None):
        """Attach an e-signature image to this document."""
        document = self.get_object()

        signature_file = request.FILES.get('signature')
        if not signature_file:
            return Response({'error': 'No signature file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        document.signature = signature_file
        document.signed_by = request.user
        document.status = 'signed'
        document.save()

        return Response(DocumentSerializer(document).data, status=status.HTTP_200_OK)