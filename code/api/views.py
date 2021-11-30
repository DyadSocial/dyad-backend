import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from api.models import Post
from api.serializers import PostSerializer


# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the api index.")

@api_view(['GET', 'POST'])
def post_user(request):
  if request.method == 'GET':
    requestUser = request.GET.get('username')
    usersPosts = Post.objects.filter(username=requestUser)
    posts_serializer = PostSerializer(usersPosts, many = True)
    return JsonResponse(posts_serializer.data, safe=False)
  elif request.method == 'POST':
    post_data = JSONParser().parse(request)
    posts_serializer = PostSerializer(data=post_data)
    if posts_serializer.is_valid():
        posts_serializer.save()
        return JsonResponse(posts_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
@api_view(['GET'])
def post_list(request):
  if request.method == 'GET':
    allPosts = Post.objects.all()
    post_serializer = PostSerializer(allPosts, many = True)
    return JsonResponse(post_serializer.data, safe= False)
    