from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    signed_by_name = serializers.CharField(source='signed_by.username', read_only=True)

    class Meta:
        model = Document
        fields = (
            'id', 'title', 'file', 'status', 'version',
            'uploaded_by', 'uploaded_by_name',
            'signature', 'signed_by', 'signed_by_name',
            'uploaded_at', 'updated_at',
        )
        read_only_fields = ('id', 'uploaded_by', 'uploaded_at', 'updated_at')