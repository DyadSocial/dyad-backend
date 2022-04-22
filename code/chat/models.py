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
    message_id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

class Chat(models.Model):
    chatid = models.CharField(max_length=25)
    participants = models.ManyToManyField(
        User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)


    def last_10_messages(self):
        return messages.order_by('-timestap').all()[:10]

    def __str__(self):
        return "{}".format(self.pk)