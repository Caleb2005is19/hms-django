# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('patient', 'Patient'),
        ('pharmacist', 'Pharmacist'),
        ('lab_tech', 'Lab Technician'),
        ('cashier', 'Cashier'),
    )
    
    # DO YOU HAVE THIS LINE BELOW? 👇
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='admin')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"