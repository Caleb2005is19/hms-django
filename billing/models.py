from django.db import models

# Create your models here.
from appointments.models import Appointment

class Bill(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Unpaid")

    def __str__(self):
        return str(self.appointment)
