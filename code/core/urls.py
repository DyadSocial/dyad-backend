from django.conf.urls import url
from django.urls import path
from core import views

urlpatterns = [
    #url(r'^core/users$', views.user_list),
    # path('test-ping/', views.test_ping),
    path('users-list/', views.DyadGetAllUsers, name="users-list"),
    path('create-user/', views.DyadCreateUser, name="create-user"),
    path('update-user/<str:pk>', views.DyadUpdateUserFields, name="update-user"),
    path('delete-user/<str:pk>', views.DyadDeleteUser, name="update-user")    
]