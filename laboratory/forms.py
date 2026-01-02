# laboratory/forms.py
from django import forms
from .models import LabRequest

class LabRequestForm(forms.ModelForm):
    class Meta:
        model = LabRequest
        fields = ['test'] # Doctor only selects the test name
        widgets = {
            'test': forms.Select(attrs={'class': 'form-select'}),
        }

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabRequest
        fields = ['result', 'status'] # Tech updates result and status
        widgets = {
            'result': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }