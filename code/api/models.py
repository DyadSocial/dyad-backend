from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.CharField(max_length=24)
    userid = models.IntegerField(default=0)
    date = models.DateTimeField('Date Created')
    optional_image = 

