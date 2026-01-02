# prescriptions/models.py
from django.db import models
from appointments.models import Appointment

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    medication = models.TextField(help_text="Doctor's notes on meds")
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 👇 ADD THIS NEW FIELD 👇
    is_dispensed = models.BooleanField(default=False)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.user.last_name}"