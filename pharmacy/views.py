# pharmacy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from prescriptions.models import Prescription
from .models import Drug
from billing.models import Invoice, InvoiceItem

@login_required
def pharmacy_dashboard(request):
    # Show only prescriptions that are NOT dispensed yet
    pending_prescriptions = Prescription.objects.filter(is_dispensed=False)
    return render(request, 'pharmacy/dashboard.html', {'prescriptions': pending_prescriptions})


@login_required
def dispense_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    drugs = Drug.objects.all() # For the dropdown list

    if request.method == 'POST':
        drug_id = request.POST.get('drug')
        quantity = int(request.POST.get('quantity'))
        
        drug = get_object_or_404(Drug, id=drug_id)
        
        # 1. Check Stock
        if drug.stock_quantity < quantity:
            return render(request, 'pharmacy/dispense.html', {
                'prescription': prescription, 
                'drugs': drugs,
                'error': f"Not enough stock! Only {drug.stock_quantity} left."
            })

        # 2. Deduct Stock
        drug.stock_quantity -= quantity
        drug.save()
        
        # 3. Add to Invoice (Find existing or create new)
        # We try to find an invoice linked to this appointment
        invoice, created = Invoice.objects.get_or_create(
            appointment=prescription.appointment,
            defaults={
                'patient': prescription.appointment.patient,
                'total_amount': 0
            }
        )
        
        total_cost = drug.price * quantity
        
        InvoiceItem.objects.create(
            invoice=invoice,
            description=f"Drug: {drug.name} (Qty: {quantity})",
            cost=total_cost
        )
        
        invoice.calculate_total()
        
        # 4. Mark Complete
        prescription.is_dispensed = True
        prescription.save()
        
        return redirect('pharmacy_dashboard')

    return render(request, 'pharmacy/dispense.html', {'prescription': prescription, 'drugs': drugs})