from django.db import models
from core.models import DyadUser

User = DyadUser()


# class Contact(models.Model):
#     user = models.ForeignKey(
#         User, related_name='friends', on_delete=models.CASCADE)
#     friends = models.ManyToManyField('self', blank=True)

#     def __str__(self):
#         return self.user.username



class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

class Chat(models.Model):
    participants = models.ManyToManyField(
        User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def last_10_messages(self):
        return Message.objects.order_by('-timestap').all()[:30]

    def __str__(self):
        return "{}".format(self.pk)