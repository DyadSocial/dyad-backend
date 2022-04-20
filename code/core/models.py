from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# this class will
# class test_ping(models.Model):
#     ping_test = "this is a simple ping"
#     #user = models.CharField(max_length = 24, unique = True)
#     #email = models.CharField(max_length = 254)
#     phone_number = PhoneNumberField(null=False, blank=False, unique=True)
#     date_created = models.DateTimeField(auto_now_add = True)
#     REQUIRED_FIELDS = ['phone_number','date_created']
class DyadGroup(Group):
    Name = models.CharField(max_length = 24, unique = True)

    
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics') #for profile picture

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path) 


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
    Display_name = models.CharField(max_length = 24)
    Profile = models.OneToOneField(DyadUser, on_delete=models.CASCADE, 
                                        primary_key=True)    

# class DyadUser2(models.Model):
#     username = models.CharField(max_length = 24, unique = True)
#     date_created = models.DateTimeField(auto_now_add = True)
#     last_active = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     phone_number = PhoneNumberField(null=False, blank=False, unique=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
