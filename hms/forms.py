# hms/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class StaffRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'user_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
        }