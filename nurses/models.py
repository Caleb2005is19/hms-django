from django.db import models
from django.conf import settings
# Create your models here.
from django.contrib.auth.models import User

class Nurse(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qualifications = models.TextField()
    phone = models.CharField(max_length=15)
    experience_years = models.IntegerField()

    def __str__(self):
        return self.user.username
    

class Ward(models.Model):
    name = models.CharField(max_length=100)
    total_beds = models.IntegerField()

    def __str__(self):
        return self.name


from patients.models import Patient

class NurseAssignment(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    shift = models.CharField(
        max_length=20,
        choices=[
            ('Morning', 'Morning'),
            ('Evening', 'Evening'),
            ('Night', 'Night')
        ]
    )
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nurse} → {self.patient}"
    


class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True)
    temperature = models.FloatField(help_text="In Celsius")
    pulse = models.IntegerField(help_text="Beats per minute")
    blood_pressure = models.CharField(max_length=20)
    oxygen_level = models.IntegerField(help_text="Percentage")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals of {self.patient}"
