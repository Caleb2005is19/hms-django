# prescriptions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from .forms import PrescriptionForm

@login_required
def add_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            
            # 👇 ADD THESE TWO LINES 👇
            appointment.status = 'completed'
            appointment.save()
            # 👆 THIS MARKS IT AS DONE 👆
            
            return redirect('dashboard')
    else:
        form = PrescriptionForm()
    
    return render(request, 'prescriptions/add_prescription.html', {'form': form, 'appointment': appointment})

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


# prescriptions/views.py
from django.shortcuts import render, get_object_or_404
from .models import Prescription

def print_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'prescriptions/print_view.html', {'prescription': prescription})