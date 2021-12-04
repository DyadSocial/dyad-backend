from django.conf.urls import url
from django.urls import path
from core import views

urlpatterns = [
    #url(r'^core/users$', views.user_list),
    path('test-ping/', views.test_ping)
]