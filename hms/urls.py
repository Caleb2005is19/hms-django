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
from pharmacy import views as pharmacy_views
from laboratory import views as lab_views
from patients import views as patient_views
from hms import views as main_views
from prescriptions import views as rx_views


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
    path('pharmacy/', pharmacy_views.pharmacy_dashboard, name='pharmacy_dashboard'),
    path('lab/order/<int:patient_id>/', lab_views.order_test, name='order_test'),
    path('lab/dashboard/', lab_views.lab_dashboard, name='lab_dashboard'),
    path('lab/process/<int:request_id>/', lab_views.process_test, name='process_test'),
    path('patient/timeline/<int:patient_id>/', patient_views.patient_timeline, name='patient_timeline'),
    path('pharmacy/dispense/<int:prescription_id>/', pharmacy_views.dispense_prescription, name='dispense_prescription'),
    path('cashier/', billing_views.cashier_dashboard, name='cashier_dashboard'),
    path('cashier/pay/<int:invoice_id>/', billing_views.process_payment, name='process_payment'),
    path('director/', main_views.admin_analytics, name='admin_analytics'),
    path('director/staff/', main_views.manage_staff, name='manage_staff'),
    path('director/staff/add/', main_views.add_staff, name='add_staff'),
    path('prescription/print/<int:prescription_id>/', rx_views.print_prescription, name='print_prescription'),
    path('search/', main_views.global_search, name='global_search'),
    


    # Dashboard
    path('', dashboard_views.index, name='dashboard'),
]