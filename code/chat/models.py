from django.db import models
from core.models import DyadUser

class Message(models.Model):
    author = models.ForeignKey(DyadUser, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages(self):
        return Message.objects.order_by('-timestap').all()[:30]