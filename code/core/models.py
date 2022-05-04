#Authors: Sam and Vincent
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# Author Sam
class DyadGroup(Group):
    Name = models.CharField(max_length = 24, unique = True)

# Author Sam
class DyadUser(User):
    date_created = models.DateTimeField(auto_now_add = True)
    last_active = models.DateTimeField(auto_now_add=True, null=True, blank=True)

# Author Sam
class DyadProfile(models.Model):
    Profile_Description = models.CharField(max_length = 200, default="BLANK", null=True)
    picture_URL = models.CharField(max_length = 200, default="", null=True)
    Display_name = models.CharField(max_length = 24)
    Profile = models.OneToOneField(DyadUser, on_delete=models.CASCADE, 
                                        primary_key=True)    
    is_moderator = models.BooleanField(default=False)
# Author Vincent
class Report(models.Model):
    reporter = models.CharField(max_length = 50)
    offender = models.CharField(max_length = 50)
    offending_title = models.CharField(max_length = 200)
    offending_content = models.CharField(max_length = 2000)
    image_url = models.CharField(max_length = 400)
    report_reason = models.CharField(max_length = 2000)
