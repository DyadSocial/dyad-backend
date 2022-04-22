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
from .serializers import ChatSerializer, GetMessagesSerializer, MessagesSerializer
from core.models import DyadUser
from rest_framework.response import Response

class ChatDetailView(APIView):

    def Chats_to_json(self, Chat):
        result = []
        for chat in Chat:
            result.append(self.Chat_to_json(chat))
        return result
    
    def Chat_to_json(self, Chat):
        return {
            'chatid': Chat.chatid,
            'participants': list(Chat.participants.all()),
            # 'messages': list(Chat.)
        }

    def post(self,request):
        serialized_data = ChatSerializer(data = request.data)
        # queryset = Chat.objects
        # serializer_class = ChatSerializer

        if serialized_data.is_valid():
            username = serialized_data.data.get('username')

#list of objects with the related participant
        Chat_objects = list(Chat.objects.filter(participants = username))

        chat_object_list = Chats_to_json(Chat_objects)

        print(chat_object_list)


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