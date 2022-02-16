from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# from django.contrib.auth import authentication
# from rest_framework.authentication import 

from .serializers import DyadUserSerializer, DyadAuthSerializer
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

from .models import DyadUser


# class LoginAPIView(GenericAPIView):

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

