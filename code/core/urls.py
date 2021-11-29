from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^core/users$', views.user_list)
]