from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


# this class will
# class test_ping(models.Model):
#     ping_test = "this is a simple ping"

class DyadUser(AbstractBaseUser):
    #user = models.CharField(max_length = 24, unique = True)
    #email = models.CharField(max_length = 254)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add = True)
    REQUIRED_FIELDS = ['phone_number','date_created']
