# appointments/models.py
from django.db import models
from doctors.models import Doctor
from patients.models import Patient

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    
    reason = models.TextField(blank=True, null=True, help_text="Reason for visit")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appt: {self.patient.user.last_name} with Dr. {self.doctor.user.last_name}"

    # 👇 THIS IS THE CRITICAL FUNCTION YOU NEED TO ADD 👇
    def has_invoice(self):
        return hasattr(self, 'invoice')