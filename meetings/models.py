from django.db import models
from django.conf import settings


class Meeting(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='meetings_organized',
        on_delete=models.CASCADE
    )
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='meetings_invited',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} ({self.organizer} -> {self.participant})"
