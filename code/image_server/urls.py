from django.urls import path, include

from image_server.views import *

urlpatterns = [
    path('upload/', imageView, name='upload'),
    path('success/', uploadSuccessView, name='success')
]