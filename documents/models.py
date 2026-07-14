from django.db import models
from django.conf import settings


class Document(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('final', 'Final'),
        ('signed', 'Signed'),
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='documents',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.PositiveIntegerField(default=1)

    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    signed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='signed_documents',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} (v{self.version}) - {self.uploaded_by}"
