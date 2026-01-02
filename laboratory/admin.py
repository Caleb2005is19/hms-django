# laboratory/admin.py
from django.contrib import admin
from .models import LabTest, LabRequest

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(LabRequest)
class LabRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'status', 'requested_at')
    list_filter = ('status', 'test')