# patients/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter

# Import all your models
from .models import Patient
from appointments.models import Appointment
from nurses.models import Vitals
from laboratory.models import LabRequest
from prescriptions.models import Prescription
from wards.models import Admission
from django.core.exceptions import PermissionDenied
from laboratory.models import LabRequest

@login_required
def patient_timeline(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    # 🔒 SECURITY CHECK 🔒
    if request.user.user_type == 'patient':
        # ERROR WAS HERE: Change 'patient_profile' to 'patient'
        # hasattr check is a safety habit in case a user has no patient record attached
        if not hasattr(request.user, 'patient') or request.user.patient != patient:
            raise PermissionDenied("You are not authorized to view this medical record.")
    # 1. Fetch all records for this patient
    appointments = Appointment.objects.filter(patient=patient)
    vitals = Vitals.objects.filter(appointment__patient=patient) # Vitals are linked via Appointment
    labs = LabRequest.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(appointment__patient=patient)
    admissions = Admission.objects.filter(patient=patient)
    
    labs = LabRequest.objects.filter(patient=patient, status='Completed').order_by('-requested_at')

    # 2. Tag them so the template knows what they are
    # We also normalize the "date" field for sorting
    for a in appointments:
        a.event_type = 'Appointment'
        # Combine date and time for sorting if needed, or just use date
        a.timeline_date = a.created_at  # Assuming you have a created_at on Appointment

    for v in vitals:
        v.event_type = 'Vitals'
        v.timeline_date = v.recorded_at

    for l in labs:
        l.event_type = 'Lab'
        l.timeline_date = l.requested_at

    for p in prescriptions:
        p.event_type = 'Prescription'
        p.timeline_date = p.created_at

    for adm in admissions:
        adm.event_type = 'Admission'
        adm.timeline_date = adm.admission_date

    # 3. Combine into one list
    timeline_events = list(chain(appointments, vitals, labs, prescriptions, admissions))

    # 4. Sort by Date (Newest first)
    # Ensure all models actually HAVE the date field we mapped above!
    timeline_events.sort(key=attrgetter('timeline_date'), reverse=True)

    return render(request, 'patients/timeline.html', {
        'patient': patient,
        'timeline': timeline_events
    })
    
    
# Inside patient_timeline view
from laboratory.models import LabRequest
# ...

# Add 'labs': labs to your context dictionary