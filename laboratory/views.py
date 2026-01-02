# laboratory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import LabRequest, LabTest
from .forms import LabRequestForm, LabResultForm
from patients.models import Patient
from billing.models import Invoice, InvoiceItem

# --- DOCTOR'S VIEW ---
@login_required
def order_test(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = LabRequestForm(request.POST)
        if form.is_valid():
            lab_req = form.save(commit=False)
            lab_req.patient = patient
            lab_req.doctor = request.user.doctor
            lab_req.save()
            return redirect('dashboard') # Back to Doctor Dashboard
    else:
        form = LabRequestForm()
    
    return render(request, 'laboratory/order_test.html', {'form': form, 'patient': patient})

# --- LAB TECH'S VIEW ---
@login_required
def lab_dashboard(request):
    # Show requests that are NOT completed yet
    pending_tests = LabRequest.objects.exclude(status='Completed').order_by('-requested_at')
    return render(request, 'laboratory/dashboard.html', {'tests': pending_tests})

@login_required
def process_test(request, request_id):
    lab_req = get_object_or_404(LabRequest, id=request_id)
    
    if request.method == 'POST':
        form = LabResultForm(request.POST, instance=lab_req)
        if form.is_valid():
            test_record = form.save(commit=False)
            if test_record.status == 'Completed':
                test_record.completed_at = timezone.now()
                
                # --- BILLING INTEGRATION ---
                # Auto-charge the patient when test is done
                invoice, created = Invoice.objects.get_or_create(
                    patient=test_record.patient,
                    paid=False,
                    defaults={'total_amount': 0}
                )
                
                InvoiceItem.objects.create(
                    invoice=invoice,
                    description=f"Lab Test: {test_record.test.name}",
                    cost=test_record.test.price
                )
                invoice.calculate_total()
                # ---------------------------

            test_record.save()
            return redirect('lab_dashboard')
    else:
        form = LabResultForm(instance=lab_req)
    
    return render(request, 'laboratory/process_test.html', {'form': form, 'lab_req': lab_req})