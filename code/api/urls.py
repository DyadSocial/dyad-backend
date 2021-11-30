from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'posts$', views.post_user),
    url(r'posts/all$', views.post_list)
]