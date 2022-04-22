# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Message, Chat 
from core.models import DyadUser
from asgiref.sync import async_to_sync
from .views import get_last_10_messages, get_user_object, check_if_in_chatlog, get_chat_object, get_last_10_messages

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = get_last_10_messages(data['roomname'])
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        # author = data['from']
        # author_user = DyadUser.objects.filter(username=author)[0]
        #FOR TESTING PURPOSES, DELETE LATER

        #make a new message object
        author_user = DyadUser.objects.filter(username = data['username'])[0]
        auther_name = DyadUser.username
        message = Message.objects.create(author=author_user,
                            content = data['message'])

        #attach that message object to the associated chatroom
        chatlog = get_chat_object(data['roomname'])
        chatlog.messages.add(message)
        chatlog.save()
        print('item saved in chatroom')

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
            'id': message.message_id,
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
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


        chatlog = Chat.objects.filter(chatid = data['roomname'])
        #print(f'room id {chatlog.chatid}')
        if chatlog:
            chatlog = chatlog[0]
        else:
            new_chatlog = Chat.objects.create(chatid = data['roomname'])
            first_person = get_user_object(data['username'])
            new_chatlog.participants.add(first_person)
            new_chatlog.save()
            chatlog = new_chatlog
            print('finished making chatlog object')
        

        check_if_in_chatlog(data['username'], chatlog)
        

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

    def send_message(self, message):

        message_list = list()
        for i in message['messages']:
            message_list.append(i)
        print(message_list)
        self.send(text_data=json.dumps(
            {
              'message':message_list  
            }
        ))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':message
        }))
