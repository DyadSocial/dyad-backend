from rest_framework import serializers
from api.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('username',
                  'title',
                  'content',
                  'date',
                  'optional_image')