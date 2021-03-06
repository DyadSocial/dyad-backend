from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/', include('chat.api.urls'))
]