# billing/forms.py
from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['total_amount', 'paid']
        widgets = {
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Amount (Ksh)'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }