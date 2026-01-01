# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# REMOVED TOP-LEVEL IMPORTS HERE to prevent circular errors

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Import models strictly inside the function
        from doctors.models import Doctor
        from patients.models import Patient
        
        if instance.user_type == 'doctor':
            Doctor.objects.create(user=instance)
        elif instance.user_type == 'patient':
            Patient.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Import models strictly inside the function
    from doctors.models import Doctor
    from patients.models import Patient

    if instance.user_type == 'doctor':
        instance.doctor.save()
    elif instance.user_type == 'patient':
        instance.patient.save()