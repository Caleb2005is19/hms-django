# wards/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from .models import Ward, Bed, Admission
from .forms import AdmissionForm # We will create this next

@login_required
def admit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            admission = form.save(commit=False)
            admission.patient = patient
            admission.admitted_by = request.user.doctor
            admission.save()
            return redirect('dashboard') # Or a 'success' page
    else:
        form = AdmissionForm()
    
    return render(request, 'wards/admit_patient.html', {'form': form, 'patient': patient})


# wards/views.py
from django.utils import timezone
from billing.models import Invoice # Import Invoice to add the room charge

# ... existing imports ...

@login_required
def discharge_patient(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)
    
    if request.method == 'POST':
        # 1. Mark as Discharged
        admission.discharge_date = timezone.now()
        admission.is_discharged = True
        admission.save()
        
        # 2. Free up the Bed
        bed = admission.bed
        bed.status = 'Available'
        bed.save()
        
        # 3. Calculate Bill (Simple Logic: Minimum 1 day charge)
        # Calculate days stayed
        duration = (admission.discharge_date - admission.admission_date).days
        if duration < 1:
            duration = 1 # Minimum 1 day charge
            
        total_cost = duration * bed.price_per_night
        
        # 4. Add to Invoice (Create one if it doesn't exist, or update existing)
        # Note: In a real app, you might want to create a new Line Item. 
        # For now, let's just create a new Invoice for the Hospital Stay.
        Invoice.objects.create(
            patient=admission.patient,
            appointment=None, # It's a ward stay, not a normal appointment
            total_amount=total_cost,
            paid=False
        )
        
        return redirect('ward_dashboard')

    return render(request, 'wards/discharge_confirm.html', {'admission': admission})

def ward_dashboard(request):
    wards = Ward.objects.all()
    # Get all active admissions (not discharged yet)
    active_admissions = Admission.objects.filter(is_discharged=False)
    return render(request, 'wards/dashboard.html', {
        'wards': wards,
        'active_admissions': active_admissions
    })
    
    
# wards/views.py
from billing.models import Invoice, InvoiceItem  # <--- Import InvoiceItem

@login_required
def discharge_patient(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)
    
    if request.method == 'POST':
        # 1. Discharge Logic
        admission.discharge_date = timezone.now()
        admission.is_discharged = True
        admission.save()
        
        bed = admission.bed
        bed.status = 'Available'
        bed.save()
        
        # 2. Create the Invoice Wrapper
        invoice = Invoice.objects.create(
            patient=admission.patient,
            admission=admission,
            paid=False
        )
        
        # 3. Calculate Ward Charges (Line Item 1)
        duration = (admission.discharge_date - admission.admission_date).days
        if duration < 1: duration = 1
        
        ward_cost = duration * bed.price_per_night
        
        InvoiceItem.objects.create(
            invoice=invoice,
            description=f"Ward Charge: {bed.ward.name} ({duration} days @ {bed.price_per_night})",
            cost=ward_cost
        )
        
        # 4. (Optional) Add a Fixed Nursing Fee (Line Item 2)
        InvoiceItem.objects.create(
            invoice=invoice,
            description="Nursing & Administrative Charges",
            cost=1500.00  # You can make this dynamic later
        )

        # 5. Update Total
        invoice.calculate_total()
        
        # Redirect to the Invoice View so they can see/print it immediately
        return redirect('view_invoice', invoice_id=invoice.id)

    return render(request, 'wards/discharge_confirm.html', {'admission': admission})