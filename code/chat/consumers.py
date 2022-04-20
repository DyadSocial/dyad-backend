# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Message 
from core.models import DyadUser
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    # def fetch_messages(self, data):
    #     messages = Message.last_10_messages(data['chatId'])
    #     content = {
    #         'messages': self.messages_to_json(messages)
    #     }
    #     self.send_message(content)

    def new_message(self, data):
        # author = data['from']
        # author_user = DyadUser.objects.filter(username=author)[0]
        print('we here')
        #FOR TESTING PURPOSES, DELETE LATER
        author_user = DyadUser.objects.all()[0]
        auther_name = DyadUser.username
        message = Message.objects.create(author=author_user,
                            content = data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        print(content["message"])
        return self.send_chat_message(content)


    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    
    def message_to_json(self,message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        #'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)
        # message = data["message"]
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )





    def send_chat_message(self, content):
        # message = data['message']
        # Send message to room group
        final_msg_string = f'({content["message"]["timestamp"]}) - {content["message"]["author"]}: {content["message"]["content"]} '
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': final_msg_string
            }
        )
        print("msg sent")

    # def send_message(self, message):
    #     self.send()

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':message
        }))