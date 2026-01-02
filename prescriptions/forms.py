# prescriptions/forms.py
from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'instructions']
        widgets = {
            'medication': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'e.g. Paracetamol 500mg, Amoxicillin 250mg'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'e.g. Take 2 tablets after meals for 5 days'
            }),
        }