from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# import json
# from rest_framework.authentication import 

from .serializers import DyadUserSerializer, DyadAuthSerializer
import jwt, datetime
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

from .models import DyadUser


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
        token = request.COOKIES.get('jwt')

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

