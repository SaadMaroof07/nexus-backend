from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'role',
                   'startup_name', 'investment_preferences')
     

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)   # yeh password ko hash karke save karta hai
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'role', 'bio', 'profile_picture',
            'location', 'date_joined',

            # Entrepreneur fields
            'startup_name', 'startup_history', 'pitch_summary',
            'funding_needed', 'industry', 'founded_year', 'team_size',

            # Investor fields
            'investment_history', 'investment_preferences', 'investment_interests',
            'investment_stage', 'portfolio_companies', 'total_investments',
            'minimum_investment', 'maximum_investment',
        )
        read_only_fields = ('id', 'email', 'role', 'date_joined')