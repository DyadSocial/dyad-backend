from django.db import models

import os
import sys
import inspect

# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

sys.path.insert(0, "/home/sam-ggez/Dyad/dyad-backend/code/core")

from core.models import DyadGroup
# Create your models here.
class Post(models.Model):
    username = models.CharField(max_length=24)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=280)
    date = models.DateTimeField('Date Created')
    image = models.ImageField(upload_to='images/%Y/%m/%d', default = None, null = True, blank = True)
    
    group_key = models.ForeignKey(DyadGroup, default = None, blank = True, null = True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


