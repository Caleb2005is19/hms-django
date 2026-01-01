from django import forms
from django.contrib.auth.models import User
from .models import Nurse

class NurseRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Nurse
        fields = ['phone', 'qualification', 'experience_years']
