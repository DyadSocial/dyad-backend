# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Message, Chat 
from core.models import DyadUser
from asgiref.sync import async_to_sync
from .views import get_last_10_messages, get_user_object, check_if_in_chatlog, get_chat_object, get_last_10_messages, make_new_chatlog



"""
FILE AUTHOR: SAM
"""    

class ChatConsumer(WebsocketConsumer):
    """
    The main component to Dyad's websocket channels for group chatting and direct messaging

    """
    def fetch_messages(self, data):
        """
        fetches and returns messages from previous existing chatlogs
        """
        messages = get_last_10_messages(data['roomname'])
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        """
        fcreates a new message, attaches to a chatlog as a many to many relationship, and
        sends it back to the active websocket chatroom
        """
        author_user = DyadUser.objects.filter(username = data['username'])[0]
        author_name = author_user.username
        message = Message.objects.create(author_id=author_user, author_name=author_name,
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
        """
        Utiliy function to turn message objects into usable json objects
        """
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    
    def message_to_json(self,message):
        """
        Turns a message object into a usable json object
        """
        return {
            'message_id': message.message_id,
            'author': message.author_id.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        """
        The first function called with a dyad websocket is called, 
        this is where a websocket connection is established
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        function called to close the entire active websocket
        """
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
            new_chatlog = make_new_chatlog(data['roomname'], data['recipients'])
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
#        final_msg_string = f'({content["message"]["timestamp"]}) - {content["message"]["author"]}: {content["message"]["content"]} '
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content["message"]["content"],
                'author': content["message"]["author"],
                'timestamp': content["message"]["timestamp"],
                'message_id': content["message"]["message_id"]
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
            'message':message,
            'author':event["author"],
			'timestamp':event["timestamp"],
            'message_id':event["message_id"]
        }))