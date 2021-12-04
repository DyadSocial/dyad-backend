from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer


@api_view(['GET'])
def test_ping(request):
    
    ping_test = "This is a test ping, the API is up and running!"

    if request.method == 'GET':
        return Response(ping_test)


# Create your views here.
