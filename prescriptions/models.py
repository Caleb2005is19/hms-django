# prescriptions/models.py
from django.db import models
from appointments.models import Appointment

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    symptoms = models.TextField(help_text="What is the patient complaining about?")
    diagnosis = models.TextField(help_text="Doctor's findings")
    medication = models.TextField(help_text="List of medicines (e.g., Paracetamol 500mg - 2x daily)")
    notes = models.TextField(blank=True, help_text="Extra advice (e.g., Drink water, Rest)")
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rx for {self.appointment.patient.user.last_name}"