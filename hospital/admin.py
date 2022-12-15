from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Pharmacist,Prescription
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

class PharmacistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Pharmacist,PharmacistAdmin)

class PrisscriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Prescription,PrisscriptionAdmin)