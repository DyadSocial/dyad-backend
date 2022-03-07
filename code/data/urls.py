from django.conf.urls import url
from django.urls import path
from core import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('image/upload', views.UploadImageView, name='upload-image'),
    path('image/query', views.QueryImageView, name='query-image'),
]
