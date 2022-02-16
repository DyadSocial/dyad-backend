from django.contrib import admin
from .models import DyadUser, DyadGroup
# Register your models here.

admin.site.register(DyadUser)
admin.site.register(DyadGroup)
