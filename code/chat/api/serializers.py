from rest_framework import serializers
from chat.models import Chat,Message
# class UserSerializer(serializers.Serializer):
#     username = serializers.Ch
    
#     model = User
#     fields = ('username',
#                 'phone',
#                 'accountCreated')

class ChatSerializer(serializers.ModelSerializer):
    # participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('username')
        # read_only = ('id')

class GetMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('chatid')
        exclude = ('participants','messages')

class MessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

    # def create(self, validated_data):
    #     participants = validated_data.pop('participants')
    #     chat = Chat()
    #     chat.save()
    #     for username in participants:
    #         contact = get_user_contact(username)
    #         chat.participants.add(contact)
    #     chat.save()
    #     return chat