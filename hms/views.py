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