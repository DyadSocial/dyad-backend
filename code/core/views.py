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


@api_view(['GET'])
#TODO: make this function require admin privileges
def get_all_users(request):

    users = DyadUser.objects.all()
    serializer = DyadUserSerializer(users, many = True)
    return Response(serializer.data)

# Create your views here.
