# wards/admin.py
from django.contrib import admin
from .models import Ward, Bed, Admission

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward_type', 'floor', 'capacity')

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'ward', 'status', 'price_per_night')
    list_filter = ('status', 'ward') # Handy sidebar filter

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'bed', 'admission_date', 'is_discharged')