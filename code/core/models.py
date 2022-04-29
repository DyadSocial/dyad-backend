from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

class DyadGroup(Group):
    Name = models.CharField(max_length = 24, unique = True)

class DyadUser(User):
    #username = models.CharField(max_length = 24, unique = True)
    #email = models.CharField(max_length = 254)
    # phone_number = PhoneNumberField(null=False, blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add = True)
    # last_active = models.DateTimeField(auto_now_add = True)
    last_active = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # is_superuser = models.BooleanField()
    # last_login = models.DateTimeField(blank = True, null = True)
    # is_staff = models.BooleanField()
    # is_active = models.BooleanField()
    # first_name = models.CharField(max_length = 150)
    # last_name = models.CharField(max_length = 150)
    # Profile = models.OneToOneField(DyadProfile, on_delete=models.CASCADE, 
    #                                     primary_key=True)
    #Dyad_Group = models.ForeignKey(DyadGroup, on_delete=models.CASCADE, blank = True, null = False)

class DyadProfile(models.Model):
    Profile_Description = models.CharField(max_length = 200, default="BLANK", null=True)
    picture_URL = models.CharField(max_length = 200, default="", null=True)
    Display_name = models.CharField(max_length = 24)
    Profile = models.OneToOneField(DyadUser, on_delete=models.CASCADE, 
                                        primary_key=True)    

# class DyadUser2(models.Model):
#     username = models.CharField(max_length = 24, unique = True)
#     date_created = models.DateTimeField(auto_now_add = True)
#     last_active = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     phone_number = PhoneNumberField(null=False, blank=False, unique=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

class Report(models.Model):
    reporter = models.CharField(max_length = 50)
    offender = models.CharField(max_length = 50)
    offending_title = models.CharField(max_length = 200)
    offending_content = models.CharField(max_length = 2000)
    image_url = models.CharField(max_length = 400)
    report_reason = models.CharField(max_length = 2000)
