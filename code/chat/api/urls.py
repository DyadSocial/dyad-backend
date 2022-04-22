from django.urls import path, re_path

from .views import (
    # ChatListView,
    ChatDetailView,
    ChatGetMessagesView
    # ChatCreateView,
    # ChatUpdateView,
    # ChatDeleteView
)

app_name = 'chat'

urlpatterns = [
    # path('', ChatListView.as_view()),
    # path('create/', ChatCreateView.as_view()),
    path('getchats/', ChatDetailView.as_view()),
    path('fetchmessages/', ChatGetMessagesView.as_view())
    # path('<pk>/update/', ChatUpdateView.as_view()),
    # path('<pk>/delete/', ChatDeleteView.as_view())
]