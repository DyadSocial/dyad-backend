from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .forms import ImageForm
from .models import Image
from .serializer import ImageSerializer

def uploadImage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Image(author=request.POST['author'], post_id=request.POST['id'], file="IMAGEDATAHERE")
            instance.save()
            return HttpResponse(json.dumps({'message': "Image has successfully been uploaded"}), status = 200)
# def uploadImage
# class ImageUploadView(generics.ListAPIView):
    # queryset  = Image.objects.all()
    # serializer_class = ImageSerializer

    # def post(self, request):
        # request.FILES
        # serializer = ImageSerializer(data = request.data)
        # serializer.is_valid()
        # serializer.save(ully been uploaded"}), status = 200)
