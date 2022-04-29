from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get(request)
        image_url = obj.fingerprint.image_url
        return request_build_absolute_uri(photo_url)