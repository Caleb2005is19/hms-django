# prescriptions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from .forms import PrescriptionForm

@login_required
def add_prescription(request, appointment_id):
    # 1. Get the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # 2. Security: Only the assigned doctor can write this
    if request.user.user_type != 'doctor' or appointment.doctor.user != request.user:
        messages.error(request, "You are not authorized to prescribe for this patient.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment  # Link it!
            prescription.save()
            
            # Auto-complete the appointment status
            appointment.status = 'completed'
            appointment.save()
            
            messages.success(request, "Prescription saved successfully!")
            return redirect('dashboard')
    else:
        form = PrescriptionForm()

    return render(request, 'prescriptions/add.html', {'form': form, 'appt': appointment})

# prescriptions/views.py
from .models import Prescription  # Ensure Prescription is imported

@login_required
def view_prescription(request, appointment_id):
    # Get the prescription linked to this appointment
    prescription = get_object_or_404(Prescription, appointment_id=appointment_id)
    
    # Security: Ensure only the involved Patient or Doctor can see this
    appt = prescription.appointment
    if request.user != appt.patient.user and request.user != appt.doctor.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    return render(request, 'prescriptions/view.html', {'rx': prescription})