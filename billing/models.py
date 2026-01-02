# billing/models.py
from django.db import models
from appointments.models import Appointment
from patients.models import Patient

class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice')
    admission = models.ForeignKey('wards.Admission', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        # Auto-sum all items linked to this invoice
        total = sum(item.cost for item in self.items.all())
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Invoice #{self.id} for {self.patient}"

# 👇 NEW MODEL FOR DETAILED CHARGES 👇
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200, help_text="e.g. Bed Charge (3 days)")
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.cost}"