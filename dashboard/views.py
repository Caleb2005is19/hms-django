# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment

@login_required
def index(request):
    user = request.user
    appointments = []

    # Logic: Fetch appointments based on who is logged in
    if user.user_type == 'doctor':
        # If I'm a doctor, get appointments where I am the doctor
        # We use 'doctor__user' because the Doctor model is linked to User
        appointments = Appointment.objects.filter(doctor__user=user)
    elif user.user_type == 'patient':
        # If I'm a patient, get appointments where I am the patient
        appointments = Appointment.objects.filter(patient__user=user)

    context = {
        'appointments': appointments,
        'user_type': user.user_type,
    }
    return render(request, 'dashboard/index.html', context)