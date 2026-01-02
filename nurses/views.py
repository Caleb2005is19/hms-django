# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from .forms import NurseRegistrationForm
from .models import Nurse

def nurse_register(request):
    if request.method == 'POST':
        form = NurseRegistrationForm(request.POST)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )

            # Assign Nurse group
            nurse_group = Group.objects.get(name='Nurse')
            user.groups.add(nurse_group)

            # Create Nurse profile
            nurse = form.save(commit=False)
            nurse.user = user
            nurse.save()

            login(request, user)
            return redirect('nurse_dashboard')
    else:
        form = NurseRegistrationForm()

    return render(request, 'nurses/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def nurse_dashboard(request):
    return render(request, 'nurses/dashboard.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from .forms import TriageForm

@login_required
def triage_queue(request):
    # Only show appointments that are confirmed but don't have vitals yet
    queue = Appointment.objects.filter(status='confirmed', vitals__isnull=True)
    return render(request, 'nurses/triage_queue.html', {'queue': queue})

# nurses/views.py

# ... imports ...

@login_required
def record_triage(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if vitals already exist to avoid crashing
    if hasattr(appointment, 'vitals'):
        return redirect('triage_queue') # Or redirect to an 'edit' page

    if request.method == 'POST':
        form = TriageForm(request.POST)
        if form.is_valid():
            try:
                vitals = form.save(commit=False)
                vitals.appointment = appointment  # Link to the specific appointment
                vitals.recorded_by = request.user.nurse # Link to the logged-in nurse
                vitals.save()
                print("✅ Vitals saved successfully!") # This prints to your terminal
                return redirect('triage_queue')
            except Exception as e:
                print(f"❌ Error saving vitals: {e}")
        else:
            print(f"⚠️ Form Invalid: {form.errors}") # Check your terminal for this!
    else:
        form = TriageForm()
    
    return render(request, 'nurses/record_triage.html', {'form': form, 'appointment': appointment})
