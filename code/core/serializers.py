from rest_framework import serializers
from .models import DyadUser

# class UserSerializer(serializers.Serializer):
#     username = serializers.Ch
    
#     model = User
#     fields = ('username',
#                 'phone',
#                 'accountCreated')

class DyadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DyadUser
        fields = '__all__'