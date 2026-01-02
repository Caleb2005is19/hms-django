# wards/models.py
from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Ward(models.Model):
    WARD_TYPES = [
        ('General', 'General Ward'),
        ('Private', 'Private Room'),
        ('ICU', 'Intensive Care Unit'),
        ('Maternity', 'Maternity Ward'),
        ('Pediatric', 'Pediatric Ward'),
    ]
    name = models.CharField(max_length=50, help_text="e.g. 'Surgical Ward A'")
    ward_type = models.CharField(max_length=20, choices=WARD_TYPES)
    capacity = models.IntegerField(default=10)
    floor = models.CharField(max_length=20, help_text="e.g. '2nd Floor'")

    def __str__(self):
        return f"{self.name} ({self.ward_type})"

class Bed(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10, help_text="e.g. 'A-101'")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.ward.name} - {self.bed_number}"

class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    admitted_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(help_text="Reason for admission")
    is_discharged = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Auto-update bed status when admitting
        if not self.pk and not self.is_discharged:
            self.bed.status = 'Occupied'
            self.bed.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admission: {self.patient.user.last_name} in {self.bed}"