from django.contrib import admin
from .models import DyadUser, DyadGroup, DyadProfile, Report
# Register your models here.

admin.site.register(DyadUser)
admin.site.register(DyadGroup)
admin.site.register(DyadProfile)
admin.site.register(Report)
