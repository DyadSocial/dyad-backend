from os.path import exists
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import os

def getPath(instance, filename):
    return 'username_{0}/{1}.{2}'.format(instance.author, instance.image_id, filename.split(".")[-1])

class Image(models.Model):
    author = models.CharField(max_length=50)
    image = models.ImageField(upload_to=getPath)
    image_id = models.CharField(max_length=50)