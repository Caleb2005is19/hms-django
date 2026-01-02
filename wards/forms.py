# wards/forms.py
from django import forms
from .models import Admission, Bed

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['bed', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bed': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # FILTER: Only show beds that are 'Available'
        self.fields['bed'].queryset = Bed.objects.filter(status='Available')
        self.fields['bed'].label_from_instance = lambda obj: f"{obj.bed_number} ({obj.ward.name}) - Ksh {obj.price_per_night}"