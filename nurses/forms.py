# nurses/forms.py
from django import forms
from .models import Nurse, Vitals

# 1. The Form for registering a Nurse Profile
class NurseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Nurse
        # These fields MUST match exactly what is in nurses/models.py
        fields = ['qualifications', 'department'] 
        widgets = {
            'qualifications': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RN, BSN'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Pediatrics'}),
        }

# 2. The Form for Triage (Vitals) - We added this earlier
class TriageForm(forms.ModelForm):
    TRIAGE_CHOICES = [
        ('stable', 'Stable (Green)'),
        ('urgent', 'Urgent (Yellow)'),
        ('emergency', 'Emergency (Red)'),
    ]
    triage_category = forms.ChoiceField(choices=TRIAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Vitals
        fields = ['temperature', 'pulse_rate', 'blood_pressure', 'weight', 'notes']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '°C'}),
            'pulse_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'BPM'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 120/80'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'kg'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }