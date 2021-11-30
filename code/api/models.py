from django.db import models

# Create your models here.
class Post(models.Model):
    username = models.CharField(max_length=24)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=280)
    date = models.DateTimeField('Date Created')
    optional_image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.title

