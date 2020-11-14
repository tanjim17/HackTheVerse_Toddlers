from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Reception)
admin.site.register(Bed)
admin.site.register(RecentMedicalData)
admin.site.register(HistoricalMedicalData)
