from rest_framework import serializers
from .models import DyadUser, DyadProfile
# class UserSerializer(serializers.Serializer):
#     username = serializers.Ch
    
#     model = User
#     fields = ('username',
#                 'phone',
#                 'accountCreated')

class DyadUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = DyadUser
        fields = ('username',
                    'password')

class DyadProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DyadProfile
        fields = '__all__'

class DyadAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = DyadUser
        fields = ('username',
                    'password')

class DyadResetPasswordSerializer(serializers.Serializer):
    model = DyadUser
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)

class DyadNewProfileSerializer(serializers.Serializer):
    model = DyadProfile
    display_name = serializers.CharField(required = True)
    profile_description = serializers.CharField(required = True)

class DyadUpdateProfileSerializer(serializers.Serializer):
    model = DyadProfile
    new_description = serializers.CharField(required = False)
    new_display_name = serializers.CharField(required = False)
    new_image = serializers.CharField(required = False)