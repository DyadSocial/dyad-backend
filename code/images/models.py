from django.db import models

# Create your models here.

class Image(models.Model):
    author = models.CharField(max_length=50)
    post_id = models.IntegerField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.author}:{self.post_id}"
    


