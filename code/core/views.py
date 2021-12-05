from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import DyadUserSerializer
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

from .models import DyadUser

# @api_view(['GET'])
# def test_ping(request):
    
#     ping_test = "This is a test ping, the API is up and running!"

#     if request.method == 'GET':
#         return Response(ping_test)

@api_view(['POST'])
def API_Overview(request):
    #TODO: returns a list of all api calls
    pass


@api_view(['GET'])
#TODO: make this function require admin privileges
def GetAllUsers(request):

    users = DyadUser.objects.all()
    serializer = DyadUserSerializer(users, many = True)
    return Response(serializer.data)

#create a new user endpoint
@api_view(['POST'])
def CreateUser(request):
    serialized_content = DyadUserSerializer(data = request.data)

    if serialized_content.is_valid():
        serialized_content.save()

    return Response(serialized_content.data)

@api_view(['POST'])
def UpdateUserFields(request):
    #TODO
    pass

@api_view(['POST'])
def UpdateUserFields(request):
    serialized_content = DyadUserSerializer(data = request.data)

    if serialized_content.is_valid():
        serialized_content.save()

    return Response(serialized_content.data)


# Create your views here.
