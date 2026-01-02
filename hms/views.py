# hms/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.utils import timezone
from appointments.models import Appointment
from patients.models import Patient
from billing.models import Invoice
from pharmacy.models import Drug
from wards.models import Bed
# hms/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required  # <--- UPDATE THIS LINE
from django.db.models import Sum, Q
from django.utils import timezone

# ... rest of your code ...

# Check if user is Superuser
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_analytics(request):
    today = timezone.now().date()

    # 1. Financials
    total_revenue = Invoice.objects.filter(paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    today_revenue = Invoice.objects.filter(paid=True, issued_at__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # 2. Patient Flow
    total_patients = Patient.objects.count()
    today_appointments = Appointment.objects.filter(date=today).count()
    
    # 3. Operations
    occupied_beds = Bed.objects.filter(status='Occupied').count()
    low_stock_drugs = Drug.objects.filter(stock_quantity__lte=10).count()

    context = {
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'occupied_beds': occupied_beds,
        'low_stock_drugs': low_stock_drugs,
    }
    return render(request, 'admin_dashboard.html', context)


# hms/views.py
from .forms import StaffRegistrationForm
from accounts.models import CustomUser
from django.shortcuts import redirect

# ... existing imports ...

@user_passes_test(is_admin)
def manage_staff(request):
    # Get all users who are NOT patients and NOT superusers
    staff_list = CustomUser.objects.exclude(user_type='patient').exclude(is_superuser=True)
    return render(request, 'director/manage_staff.html', {'staff_list': staff_list})

@user_passes_test(is_admin)
def add_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_staff')
    else:
        form = StaffRegistrationForm()
    
    return render(request, 'director/add_staff.html', {'form': form})


# hms/views.py
from django.db.models import Q
from patients.models import Patient
from accounts.models import CustomUser
from billing.models import Invoice

# ... existing imports ...

@login_required
def global_search(request):
    query = request.GET.get('q')
    
    if not query:
        return redirect('dashboard')

    # 1. Search Patients (First Name, Last Name, or ID)
    patients = Patient.objects.filter(
        Q(user__first_name__icontains=query) | 
        Q(user__last_name__icontains=query) |
        Q(id__icontains=query)
    )

    # 2. Search Staff/Doctors (Username or Name)
    staff = CustomUser.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    ).exclude(user_type='patient')

    # 3. Search Invoices (ID)
    # Check if query is a number before searching ID fields
    invoices = []
    if query.isdigit():
        invoices = Invoice.objects.filter(id=query)

    context = {
        'query': query,
        'patients': patients,
        'staff': staff,
        'invoices': invoices,
    }
    return render(request, 'search_results.html', context)