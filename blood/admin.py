from django.contrib import admin

# Register your models here.


from .models import BloodRequest,Patient2,Stock

admin.site.register(BloodRequest)
admin.site.register(Patient2)
admin.site.register(Stock)