# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add our custom fields to the admin display
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'phone_number', 'profile_pic', 'address')}),
    )
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name']
    list_filter = ['user_type']

admin.site.register(CustomUser, CustomUserAdmin)