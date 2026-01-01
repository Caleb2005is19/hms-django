# billing/forms.py
from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['item_list', 'total_amount']
        widgets = {
            'item_list': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'e.g. Consultation Fee, Panadol'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1500.00'}),
        }