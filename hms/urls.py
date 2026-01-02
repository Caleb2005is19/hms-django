# hms/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from dashboard import views as dashboard_views
from appointments import views as appointment_views
from prescriptions import views as rx_views
from billing import views as billing_views
from nurses import views as nurse_view
from wards import views as ward_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth URLs
    path('register/', account_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('book-appointment/', appointment_views.book_appointment, name='book_appointment'),
    path('update-appt/<int:appointment_id>/<str:new_status>/', appointment_views.update_status, name='update_status'),
    path('prescribe/<int:appointment_id>/', rx_views.add_prescription, name='add_prescription'),
    path('prescription/view/<int:appointment_id>/', rx_views.view_prescription, name='view_prescription'),
    path('billing/generate/<int:appointment_id>/', billing_views.generate_invoice, name='generate_invoice'),
    path('billing/pay/<int:invoice_id>/', billing_views.pay_invoice, name='pay_invoice'),
    path('nurse/queue/', nurse_view.triage_queue, name='triage_queue'),
    path('nurse/record/<int:appointment_id>/', nurse_view.record_triage, name='record_triage'),
    path('admit/<int:patient_id>/', ward_views.admit_patient, name='admit_patient'),
    path('wards/', ward_views.ward_dashboard, name='ward_dashboard'),
    path('wards/discharge/<int:admission_id>/', ward_views.discharge_patient, name='discharge_patient'),
    path('invoice/<int:invoice_id>/', billing_views.view_invoice, name='view_invoice'),


    # Dashboard
    path('', dashboard_views.index, name='dashboard'),
]