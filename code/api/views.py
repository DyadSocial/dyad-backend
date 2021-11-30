import json
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the api index.")

@api_view(['GET', 'POST'])
def post_list(request):
  if request.method == 'GET':
    requestUser = request.GET.get('username')
    post = Post.objects.filter(username=requestUser)
    posts_serializer = PostSerializer(posts, many = True)
    return JsonResponse(post_serializer.data, safe=False)
  elif request.method == 'POST':
    post_data = JSONParser().parse(request)
    posts_serializer = PostSerializer(data=user_data)
    if posts_serializer.is_valid():
        posts_serializer.save()
        return JsonResponse(postss_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(postss_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
