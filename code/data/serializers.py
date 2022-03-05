from rest_framework import serializers
from django.contrib.auth.models import User
from django_grpc_framework import proto_serializers
from protos.image_pb2 import ImageChunk

# class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    # class meta:
        # model = User
        # proto_class = ImageChunk
        # fields = ['name
