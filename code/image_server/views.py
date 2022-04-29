from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from image_server.forms import ImageForm
from django.views.decorators.csrf import csrf_exempt
from .models import Image
from .serializers import ImageSerializer

# Create your views here.
@csrf_exempt
def imageView(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("VALID")
            form.save()
            img_obj = form.instance
            #queryset = Image.objects.all()
            serializer = ImageSerializer(img_obj)
            print("SERIALIZER")
            print(serializer.data)
            return JsonResponse(serializer.data, status=200)
    else:
        form = ImageForm()
    return HttpResponse(f"https://api.dyadsocial.com/")

def uploadSuccessView(request):
    return HttpResponse('Upload Success')