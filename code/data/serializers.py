from rest_framework import serializers
from django.contrib.auth.models import User
from django_grpc_framework import proto_serializers
import data.protos.image_pb2 as imageChunkProto

class ImageChunkProtoSerializer(proto_serializers.ModelProtoSerializer):
    class meta:
        model = User
        proto_class = imageChunkProto.ImageChunk
        fields = ['imageData', 'size']

