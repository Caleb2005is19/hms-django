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

# billing/views.py
from django.shortcuts import render, get_object_or_404
from .models import Invoice

def view_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})

# billing/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Invoice

@login_required
def cashier_dashboard(request):
    # Get all unpaid invoices (Newest first)
    pending_invoices = Invoice.objects.filter(paid=False).order_by('-issued_at')
    return render(request, 'billing/cashier_dashboard.html', {'invoices': pending_invoices})

@login_required
def process_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        # Mark as Paid
        invoice.paid = True
        invoice.save()
        
        # In a real system, you might record "Payment Method" (Cash/M-Pesa) here
        # For now, we just mark it as cleared.
        
        return redirect('view_invoice', invoice_id=invoice.id) # Show the Receipt

    return render(request, 'billing/process_payment.html', {'invoice': invoice})