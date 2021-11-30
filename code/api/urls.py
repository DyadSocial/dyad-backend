from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'posts$', views.post_list)
]