# pharmacy/admin.py
from django.contrib import admin
from .models import Drug

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock_quantity', 'price', 'expiry_date', 'is_low_stock')
    search_fields = ('name',)
    list_filter = ('expiry_date',)