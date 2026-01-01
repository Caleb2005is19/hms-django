# billing/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from appointments.models import Appointment
from .models import Invoice
from .forms import InvoiceForm

@login_required
def generate_invoice(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if invoice already exists
    if hasattr(appointment, 'invoice'):
        messages.warning(request, "Invoice already exists for this appointment.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.appointment = appointment
            invoice.save()
            messages.success(request, "Invoice generated successfully!")
            return redirect('dashboard')
    else:
        # Auto-fill standard consultation fee
        form = InvoiceForm(initial={'item_list': 'Consultation Fee', 'total_amount': 1000})

    return render(request, 'billing/generate.html', {'form': form, 'appt': appointment})

@login_required
def pay_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Simulate Payment
    invoice.paid = True
    invoice.paid_at = timezone.now()
    invoice.save()
    
    messages.success(request, f"Invoice #{invoice.id} paid successfully!")
    return redirect('dashboard')