import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from api.models import Post
from api.serializers import PostSerializer
from rest_framework.response import Response


# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the api index.")

@api_view(['GET', 'POST'])
def post_user(request):
  requestUser = request.GET.get('username')
  if request.method == 'GET':
    usersPosts = Post.objects.all()
    posts_serializer = PostSerializer(usersPosts, many = True)
    # return JsonResponse(posts_serializer.data, safe=False)
    return Response(posts_serializer.data)
  elif request.method == 'POST':
    # post_data = JSONParser().parse(request)
    posts_serializer = PostSerializer(data=request.data)
    if posts_serializer.is_valid():
        posts_serializer.save()
        return Response(posts_serializer.data)
    else:
        return Response(posts_serializer.errors)
  elif request.method == 'DELETE':
    userDeletePost = Post.objects.filter(username = requestUser)
    userDeletePost.delete()

    return HttpResponse("Successfully deleted post!")

@api_view(['DELETE'])
def DeletePost(request, pk):
  userDeletePost = Post.objects.get(id = pk)
  userDeletePost.delete()
  stri = "Succesfully Deleted Post!"
  return Response(stri)


      
@api_view(['GET'])
def post_list(request):
  if request.method == 'GET':
    allPosts = Post.objects.all()
    post_serializer = PostSerializer(allPosts, many = True)
    return JsonResponse(post_serializer.data, safe= False)
    