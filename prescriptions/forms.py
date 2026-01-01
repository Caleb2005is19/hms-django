# prescriptions/forms.py
from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['symptoms', 'diagnosis', 'medication', 'notes']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'medication': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }