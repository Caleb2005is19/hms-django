# appointments/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # 1. Auto-assign the Patient (You)
            appointment.patient = request.user.patient
            
            # 2. Set default status
            appointment.status = 'pending'
            
            appointment.save()
            messages.success(request, 'Appointment request sent successfully!')
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book.html', {'form': form})


# appointments/views.py
from django.shortcuts import get_object_or_404

# ... (keep your other imports and functions) ...

@login_required
def update_status(request, appointment_id, new_status):
    # Security: Get the appointment OR return 404 error if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Security: Ensure only the ASSIGNED doctor can touch this
    if request.user.user_type == 'doctor' and appointment.doctor.user == request.user:
        if new_status in ['confirmed', 'cancelled']:
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Appointment {new_status} successfully!")
    
    return redirect('dashboard')