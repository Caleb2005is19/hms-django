# nurses/models.py
from django.db import models
from django.conf import settings
from appointments.models import Appointment

class Nurse(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nurse')
    qualifications = models.CharField(max_length=100, help_text="e.g. BSN, RN, CNA")
    department = models.CharField(max_length=100, help_text="e.g. Pediatrics, ICU")

    def __str__(self):
        return f"Nurse {self.user.last_name} ({self.department})"

class Vitals(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='vitals')
    recorded_by = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True)
    
    # Vital Signs
    temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text="°C")
    pulse_rate = models.IntegerField(help_text="BPM")
    respiration_rate = models.IntegerField(default=16, help_text="Breaths/min")
    blood_pressure = models.CharField(max_length=20, help_text="e.g. 120/80")
    oxygen_saturation = models.IntegerField(default=98, help_text="SpO2 %")
    
    # Body Measurements
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="meters")
    
    notes = models.TextField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.appointment.patient.user.last_name}"