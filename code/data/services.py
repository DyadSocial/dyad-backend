import grpc
from django_grpc_framework.services import Service
from data.serializers import ImageChunkSerializer
from data.models import Image

"""
  gRPC Service allowing images to be uploaded
"""
class ImageService(Service):
    def uploadImage(self, request):
        print('Received Request for ImageUpload')



