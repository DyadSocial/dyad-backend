from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from chat.models import Chat, Message
from chat.views import get_last_10_messages
from .serializers import ChatSerializer, GetMessagesSerializer, MessagesSerializer, UserSerializer
from core.models import DyadUser
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

class ChatDetailView(APIView):

    def Chats_to_json(self, Chat_object):
        result = []
        print(f'fffff {Chat_object}')
        for chat in Chat_object:
            result.append(self.Chat_to_json(chat))
        return result
    
    def Chat_to_json(self, Chat_object):
        
        participants = Chat_object.participants.all()
        
        participant_list_strings = list()
        for i in participants:
                participant_list_strings.append(i.username)
        
        participant_list_strings.sort()
        return {
            'chatid': Chat_object.chatid,
            'participants': participant_list_strings,
            # 'messages': list(Chat.)
        }

    def post(self,request):
        # serialized_data = ChatSerializer(data = request.data)
        # # queryset = Chat.objects
        # # serializer_class = ChatSerializer

        # if serialized_data.is_valid():
        #     username = serialized_data.data.get('username')

#list of objects with the related participant
        username = request.data["username"]

        Chat_objects = list(Chat.objects.filter(participants__username__startswith = username))
        chat_object_list = self.Chats_to_json(Chat_objects)
        print(chat_object_list)


        return Response(chat_object_list)
        


class ChatGetMessagesView(APIView):

    def post(self,request):
        print(f'herer{request.data}')
        # serialized_data = GetMessagesSerializer(data=request.data)

        # if serialized_data.is_valid():
        #     chatid = serialized_data.data.get('chatid')

        chatid = request.data["chatid"]
        print(chatid)
        chat_object = Chat.objects.filter(chatid=chatid)[0]
        chat_object_size = len(list(chat_object.messages.all()))
        print(chat_object_size)
        if chat_object_size < 10:
            last_10_messages = chat_object.messages.order_by('-timestamp')[:chat_object_size]
        else:
            last_10_messages = chat_object.messages.order_by('-timestamp')[:10]

        return_serialized_data = MessagesSerializer(list(last_10_messages), many=True)

        print(return_serialized_data.data)


        return Response(return_serialized_data.data)

class CheckUserExistView(APIView):

    def post(self,request):

        try:
            DyadUser.objects.filter(username = request["username"])
            return Response({
                "status": status.HTTP_200_OK,
                "Message": "The requested user does exist in the database"
            })
        except ObjectDoesNotExist:
            return Response({
                "status": status.HTTP_404_OK,
                "Message":"The requested user does not exist!"
            })


        # for i in Chat_objects:

        #     participants_list = list()

        #     for j in Chat_objects:


        #     json_template = {
        #         'chatid':i['chatid'],
        #         'participants':
        #     }



# class ChatListView(ListAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.AllowAny, )

#     def get_queryset(self):
#         queryset = Chat.objects.all()
#         username = self.request.query_params.get('username', None)
#         if username is not None:
#             contact = get_user_contact(username)
#             queryset = contact.chats.all()
#         return queryset


# class ChatDetailView(RetrieveAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.AllowAny, )


# class ChatCreateView(CreateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.IsAuthenticated, )


# class ChatUpdateView(UpdateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.IsAuthenticated, )


# class ChatDeleteView(DestroyAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.IsAuthenticated, )
