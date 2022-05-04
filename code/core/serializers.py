from rest_framework import serializers
from .models import DyadUser, DyadProfile, Report
# class UserSerializer(serializers.Serializer):
#     username = serializers.Ch
    
#     model = User
#     fields = ('username',
#                 'phone',
#                 'accountCreated')



class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer method for report data
    Author: Vincent
    """
    class Meta :
        model = Report
        fields = '__all__'

class DyadUserSerializer(serializers.ModelSerializer):
    """
    Serializer method for Dyad user data, also creates new users in the database
    Author: Sam
    """
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
    """
    Serializer method for Dyad profile data
    Author: Sam
    """
    class Meta:
        model = DyadProfile
        fields = '__all__'

class DyadAuthSerializer(serializers.ModelSerializer):
    """
    Serializer method for Dyad Auth data
    Author: Sam
    """
    class Meta:
        model = DyadUser
        fields = ('username',
                    'password')

class DyadResetPasswordSerializer(serializers.Serializer):
    """
    Serializer method for password reset data 
    Author: Sam
    """
    model = DyadUser
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)

class DyadNewProfileSerializer(serializers.Serializer):
    """
    Serializer method for new dyad profile data
    Author: Sam
    """
    model = DyadProfile
    display_name = serializers.CharField(required = True)
    profile_description = serializers.CharField(required = True)

class DyadUpdateProfileSerializer(serializers.Serializer):
    """
    Serializer method for updating dyad profile data
    Author: Sam
    """
    model = DyadProfile
    new_description = serializers.CharField(required = False)
    new_display_name = serializers.CharField(required = False)
    new_image = serializers.CharField(required = False)