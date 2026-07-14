from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    # Columns shown in the user list page
    list_display = ('id', 'email', 'username', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'startup_name')
    ordering = ('-date_joined',)

    # Fields shown when editing an existing user
    fieldsets = (
        (None, {'fields': ('id', 'email', 'username', 'password')}),
        ('Personal Info', {'fields': ('bio', 'profile_picture', 'location')}),
        ('Role', {'fields': ('role',)}),
        ('Entrepreneur Info', {'fields': (
            'startup_name', 'startup_history', 'pitch_summary',
            'funding_needed', 'industry', 'founded_year', 'team_size'
        )}),
        ('Investor Info', {'fields': (
            'investment_history', 'investment_preferences', 'investment_interests',
            'investment_stage', 'portfolio_companies', 'total_investments',
            'minimum_investment', 'maximum_investment'
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when creating a NEW user from admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('id', 'last_login', 'date_joined')


admin.site.register(User, CustomUserAdmin)