from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # url(r'posts$', views.post_user),
    # url(r'posts/all$', views.post_list)
    path('post-user/', views.post_user, name = "post-user"),
    # path('post-user/<str:pk>', views.post_user, name = "post-user")
    path('delete-post/<str:pk>', views.delete_post, name = "delete-user")    
]