from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from images import views
# from dyadchat.views import index

urlpatterns = [
    path('upload/', csrf_exempt(views.uploadImage), name="image-upload"),
    ]
