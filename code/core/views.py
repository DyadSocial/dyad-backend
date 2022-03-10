from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics


from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django_rest_passwordreset.signals import reset_password_token_created

from .serializers import DyadUserSerializer, DyadAuthSerializer, DyadResetPasswordSerializer, DyadNewProfileSerializer, DyadUpdateProfileSerializer, DyadProfileSerializer
from django.core import serializers as serial
import jwt, datetime
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

from .models import DyadUser, DyadProfile

class RegisterView(APIView):
    
    def post(self, request):
        serializer = DyadUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        response = Response()

        response.data = {
            'message: The User has been successfully created!'
        }

        return response

class LoginView(APIView):
    
    def post(self,request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = DyadUser.objects.filter(username = username).first()

        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password for user!")


        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm = 'HS256')

        response = Response()

        response.set_cookie(key='jwt', value = token, httponly=True)
        response.data = {
            'jwt':token
        }    

        return response

class UserView(APIView):

    def get(self,request):
        token = request.headers.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, Cookie expire')
        
        user = User.objects.filter(id = payload['id']).first()

        serializer = DyadUserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response

class CreateDyadProfileView(generics.CreateAPIView):


    """
    End point to create a new dyad profile object.
    This endpoint should only ever be called one time per newly created user
    """

    serializer_class = DyadNewProfileSerializer
    model = DyadUser
    permission_class = ('IsAuthenticated')

    def get_object(self, queryset = None):
        token = self.request.headers.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, Cookie expired')
        
        user = User.objects.filter(id = payload['id']).first()

        return user

    def post(self,request):
        userobj = self.get_object()
        Dyaduser = DyadUser.objects.get(username=userobj.username)

        serialized_data = DyadNewProfileSerializer(data = request.data)
        
        if serialized_data.is_valid():
            new_profile = DyadProfile(Profile = Dyaduser, 
                                        Profile_Description = serialized_data.data.get('profile_description'),
                                        Display_name = serialized_data.data.get('display_name')
                                        )
            new_profile.save()
        else:
            return Response({"message":"Data provided isn't valid serializer data, please try again"}, status=status.HTTP_400_BAD_REQUEST)        

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Your Dyad profile has been successfully created',
            'data': []
        }

        return Response(response)

class GetDyadProfileView(generics.ListAPIView):

    serializer_class = DyadProfileSerializer
    model = DyadUser
    permission_class = ('IsAuthenticated')

    def get_object(self, queryset = None):
        token = self.request.headers.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, Cookie expired')
        
        user = User.objects.filter(id = payload['id']).first()

        return user
    
    def get(self, request):
        userobj = self.get_object()
        Dyaduser = DyadUser.objects.get(username=userobj.username)

        
        Update_Dyad_Profile = DyadProfile.objects.get(Profile = Dyaduser)

        serialized_data = DyadProfileSerializer(Update_Dyad_Profile)

        return Response(serialized_data.data)

class UpdateDyadProfileView(generics.UpdateAPIView):
    
    serializer_class = DyadUpdateProfileSerializer
    model = DyadUser
    permission_class = ('IsAuthenticated')

    def get_object(self, queryset = None):
        token = self.request.headers.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, Cookie expired')
        
        user = User.objects.filter(id = payload['id']).first()

        return user
    
    def update(self, request):
        userobj = self.get_object()
        Dyaduser = DyadUser.objects.get(username=userobj.username)

        serialized_data = self.get_serializer(data = request.data)

        if serialized_data.is_valid():
            pass
        else:
            return Response({"message":"Data provided isn't valid serializer data, please try again"}, status=status.HTTP_400_BAD_REQUEST)          

        Update_Dyad_Profile = DyadProfile.objects.get(Profile = Dyaduser)

        if serialized_data.data.get("new_description"):
            Update_Dyad_Profile.Profile_Description = serialized_data.data.get("new_description")
        if serialized_data.data.get("new_display_name"):
            Update_Dyad_Profile.Display_name = serialized_data.data.get("new_display_name")
        Update_Dyad_Profile.save()
    
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Dyad Profile Successfully Updated!',
            'data': []
        }

        return Response(response)
          
class PasswordResetTokenView(generics.UpdateAPIView):

    """

    Class for generating token for password resetting of 
    a user account

    """
    
    serializer_class = DyadResetPasswordSerializer
    model = DyadUser
    permission_class = ('IsAuthenticated')

    def get_object(self, queryset = None):
        token = self.request.headers.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, Cookie expired')
        
        user = User.objects.filter(id = payload['id']).first()

        return user

    def update(self, request):
        user_object = self.get_object()
        serialized_data = self.get_serializer(data = request.data)

        # check if data is valid
        # if so, check for old password
        if serialized_data.is_valid():
            if not user_object.check_password(serialized_data.data.get("old_password")):
                response = {
                    "user": f'{user_object.username}', #NOTICE: DELETE THIS DURING PRODUCTION
                    "old_password": "Invalid",
                    "notice": "NOTICE: the provided password is incorrect, please try again"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Data provided isn't valid serializer data, please try again"}, status=status.HTTP_400_BAD_REQUEST)
        user_object.set_password(serialized_data.data.get("new_password"))
        user_object.save()
        
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully!',
            'data': []
        }

        return Response(response)



@api_view(['POST'])
def API_Overview(request):
    #TODO: returns a list of all api calls
    # make a list of  API overviews
    pass


@api_view(['GET'])
#TODO: make this function require admin privileges
def DyadGetAllUsers(request):
    users = DyadUser.objects.all()
    serializer = DyadUserSerializer(users, many = True)
    return Response(serializer.data)

#create a new user endpoint
@api_view(['POST'])
def DyadCreateUser(request):
    serialized_content = DyadUserSerializer(data = request.data)

    if serialized_content.is_valid():
        # newuser = DyadUser(username=serialized_content["username"],
        #                     password=serialized_content["password"])
        # serialized_content.save()
        # set_pass_user = DyadUser.objects.filter(username="")
        # newuser.save()
        serialized_content.save()
        return Response(serialized_content.data["username"])
    else:
        return Response("Not saved correctly")



@api_view(['POST'])
def DyadUpdateUserFields(request, pk):
    update_user = DyadUser.objects.get(id = pk)
    serialized_content = DyadUserSerializer(instance = update_user,data = request.data)

    if serialized_content.is_valid():
        serialized_content.save()    

    return Response(serialized_content.data)

@api_view(['DELETE'])
def DyadDeleteUser(request, pk):
    delete_user = DyadUser.objects.get(id = pk)
    delete_user.delete()
    return Response("Successfully deleted user!")



# @api_view(['POST'])
# def DyadLoginAuth(request):
#     serialized_content = DyadAuthSerializer(data = request.data)

#     if serialized_content.is_valid():
#         if DyadUser.objects.filter(username = serialized_content["username"]).exists():

        




# #Testing JWT auth
# @api_view(['POST'])
# def DyadLoginAuth(request):

