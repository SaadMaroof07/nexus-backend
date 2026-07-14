from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('entrepreneur', 'Entrepreneur'),
        ('investor', 'Investor'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    # ---------- Entrepreneur-specific ----------
    startup_name = models.CharField(max_length=255, blank=True, null=True)
    startup_history = models.TextField(blank=True, null=True)
    pitch_summary = models.TextField(blank=True, null=True)
    funding_needed = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    team_size = models.IntegerField(blank=True, null=True)

    # ---------- Investor-specific ----------
    investment_history = models.TextField(blank=True, null=True)
    investment_preferences = models.TextField(blank=True, null=True)
    investment_interests = models.JSONField(default=list, blank=True)   # e.g. ["FinTech", "SaaS"]
    investment_stage = models.JSONField(default=list, blank=True)       # e.g. ["Seed", "Series A"]
    portfolio_companies = models.JSONField(default=list, blank=True)    # e.g. ["Company A", "Company B"]
    total_investments = models.IntegerField(default=0)
    minimum_investment = models.CharField(max_length=50, blank=True, null=True)
    maximum_investment = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"