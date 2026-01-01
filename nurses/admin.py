from django.contrib import admin

# Register your models here.
from .models import Nurse, Ward, NurseAssignment, VitalSigns

admin.site.register(Nurse)
admin.site.register(Ward)
admin.site.register(NurseAssignment)
admin.site.register(VitalSigns)
