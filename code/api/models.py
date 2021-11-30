from django.db import models

# Create your models here.
class Post(models.Model):
    username = models.CharField(max_length=24)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=280)
    date = models.DateTimeField('Date Created')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank = True)
    
    def __str__(self):
        return self.title

