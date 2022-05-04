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
from core.forms import *


from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django_rest_passwordreset.signals import reset_password_token_created

from .serializers import DyadUserSerializer, DyadAuthSerializer, DyadResetPasswordSerializer, DyadNewProfileSerializer, DyadUpdateProfileSerializer, DyadProfileSerializer, ReportSerializer
from django.core import serializers as serial
import jwt, datetime

from .models import DyadUser, DyadProfile, Report

class RegisterView(APIView):
    """
    This API endpoint generates a new user into the database

    Author: Sam

    Parameters
    ----------
    data["username"]: str, the username of the new user
    data["password"]: str, the password of the new user, backend
                            takes care of encryption and hashing

    """
    
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
    """
    API endpoint for handling login auth

    Author: Sam

    Paremeters
    ----------
    data["username"]: str, the username of the auth user
    data["password"]: str, the pasword of the auth user

    Returns
    -------
    "JWT": Json Web Token, used for identificaiton and auth
                            on Dyad platforms
    """
    
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
    """
    A basic API endpoint for grabbing the display name, description,
    and other information on a user

    Author: Sam

    Auth
    ----
    JWT: Requires a valid JWT of the user, otherwise returns
            an authentication failed
    """

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
    """
    API auth logout view, essentially deletes your JWT for you

    Author: Sam

    Parameters
    ----------
    JWT: The Json Web Token that will be deleted by the backend
    """
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response

"""
End point to report a User with their offending content, their offending post
"""
class ReportView(generics.CreateAPIView):
    """
    API endpoint for reporting users who have malicious/suspicious post

    Author: Vincent

    Auth
    ----
    "JWT": the Json web token of the user making the reqeust

    Parameters
    ----------
    data["offender"]: str, username of the post getting reported
    data["offending_title"]: str, title of the post getting reported
    data["offending_content]: str, body content of the post
    data["image_url"]: str, image of the post
    data["report_reason"]: str, body content of the report reason submitted
    """
    serializer = ReportSerializer
    model = Report
    permission_class = ('IsAuthenticated')
    def get_object(self, queryset = None):
        token = self.request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, Cookie expired')
        user = User.objects.filter(id = payload['id']).first()
        return user

    def post(self, request):
        userobj = self.get_object()
        serialized_data = ReportSerializer(data = request.data)
        print(serialized_data.initial_data)
        new_report = Report(
            reporter = userobj.username,
            offender = serialized_data.initial_data.get('offender'),
            offending_title = serialized_data.initial_data.get('offending_title'),
            offending_content = serialized_data.initial_data.get('offending_content'),
            image_url = serialized_data.initial_data.get('image_url'),
            report_reason = serialized_data.initial_data.get('report_reason'),
            )
        new_report.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Report received'
        }

        return Response(response)


class CreateDyadProfileView(generics.CreateAPIView):
    """
    End point to create a new dyad profile object.
    This endpoint should only ever be called one time per newly created user

    Author: Sam

    Auth
    ----
    "JWT", used for authentication and Identifcation 

    Returns
    -------
    DyadProfile: model object, is the object representing the display name
                                and description information of a new user

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
                                        picture_URL = serialized_data.data.get('picture_url'),
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
    """
    API end for getting the Dyad profile object of a user

    Author: Sam

    Auth
    ----
    "JWT": for authentication and identification

    Return
    ------
    data["display_name"]: str, the display named used on the dyad application of a user object
    data["dyad_description"]: str, the profile description of a user object
    """

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
        
        print(self.request.GET.get("username"))
        if self.request.GET.get("username") is None:
            user = User.objects.filter(id = payload['id']).first()
        else:
            try:
                user = User.objects.filter(username = self.request.GET.get("username")).first()
            except:
                user = None

        return user
    
    def get(self, request):
        userobj = self.get_object()
        Dyaduser = DyadUser.objects.get(username=userobj.username)

        
        Update_Dyad_Profile = DyadProfile.objects.get(Profile = Dyaduser)

        serialized_data = DyadProfileSerializer(Update_Dyad_Profile)

        return Response(serialized_data.data)

class UpdateDyadProfileView(generics.UpdateAPIView):
    """
    Basic API endpoint for updating a users dyad profile

    Author: Sam

    Auth
    ----
    "JWT": for authentication and identification

    Return
    ------
    HTTP_200: The profile was successfully updated
    HTTP_400: the profile was not updated because of lack of proper auth
    """
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
        if serialized_data.data.get("new_image"):
            Update_Dyad_Profile.picture_URL = serialized_data.data.get("new_image")
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

    Author: Sam

    Auth
    ----
    "JWT": Required auth

    Parameters
    ----------
    data["password"]: str, user needs to enter their password regardless of JWT auth
    data["new_password"]: str, the new password of the user object

    Returns
    -------
    HTTP_200: password was successfully changed
    HTTP_400: password was not successfully changed because of lack of auth
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


# =========UNUSED/DEPRECATED FUNCTION===========
@api_view(['POST'])
def API_Overview(request):
    #TODO: returns a list of all api calls
    # make a list of  API overviews
    pass

# =========UNUSED/DEPRECATED FUNCTION===========
@api_view(['GET'])
#TODO: make this function require admin privileges
def DyadGetAllUsers(request):
    users = DyadUser.objects.all()
    serializer = DyadUserSerializer(users, many = True)
    return Response(serializer.data)

# =========UNUSED/DEPRECATED FUNCTION===========
#create a new user endpoint
@api_view(['POST'])
def DyadCreateUser(request):
    serialized_content = DyadUserSerializer(data = request.data)

    if serialized_content.is_valid():
        serialized_content.save()
        return Response(serialized_content.data["username"])
    else:
        return Response("Not saved correctly")


# =========UNUSED/DEPRECATED FUNCTION===========
@api_view(['POST'])
def DyadUpdateUserFields(request, pk):
    update_user = DyadUser.objects.get(id = pk)
    serialized_content = DyadUserSerializer(instance = update_user,data = request.data)

    if serialized_content.is_valid():
        serialized_content.save()    

    return Response(serialized_content.data)

# =========UNUSED/DEPRECATED FUNCTION===========
@api_view(['DELETE'])
def DyadDeleteUser(request, pk):
    delete_user = DyadUser.objects.get(id = pk)
    delete_user.delete()
    return Response("Successfully deleted user!")

def reportUser(request):
    """
    request form method for reporting a user
    Author: Vincent
    """
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()


        




# #Testing JWT auth
# @api_view(['POST'])
# def DyadLoginAuth(request):

