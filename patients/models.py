# patients/models.py
from django.db import models
from django.conf import settings

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Make these optional for signup
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    medical_history = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"