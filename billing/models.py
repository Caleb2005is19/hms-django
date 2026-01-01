# billing/models.py
from django.db import models
from appointments.models import Appointment

class Invoice(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='invoice')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    item_list = models.TextField(help_text="Items charged (e.g., Consultation, Drugs)")
    paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.appointment.patient.user.last_name}"