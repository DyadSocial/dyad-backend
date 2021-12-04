from django.db import models
from django.contrib.auth import
from phonenumber)field.modefiels import PhoneNumberField


# this class will
# class test_ping(models.Model):
#     ping_test = "this is a simple ping"

class DyadUser(models.AbstractBaseUser):
    user = models.Charfield(max_length = 24, unique = True)
    email = models.CharField(max_length = 254)
    phone_number = PhoneNumberField()
    date_created = models.DateTimeField(auto_now_add)

    USERNAME_FIELD = user
    EMAIL_FIELD = email
