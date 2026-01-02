# nurses/admin.py
from django.contrib import admin
from .models import Nurse, Vitals

admin.site.register(Nurse)
admin.site.register(Vitals)