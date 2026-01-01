# doctors/models.py
from django.db import models
from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # We add null=True and blank=True so the Signal can create an empty profile first
    specialization = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=100, null=True, blank=True)
    available_days = models.CharField(max_length=100, null=True, blank=True)
    
    # These were the specific ones causing the crash:
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.last_name} - {self.specialization or 'No Spec'}"