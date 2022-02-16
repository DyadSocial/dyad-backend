from django.conf.urls import url
from django.urls import path
from core import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    #url(r'^core/users$', views.user_list),
    # path('test-ping/', views.test_ping),
    path('users-list/', views.DyadGetAllUsers, name="users-list"),
    path('create-user/', views.DyadCreateUser, name="create-user"),
    path('update-user/<str:pk>', views.DyadUpdateUserFields, name="update-user"),
    path('delete-user/<str:pk>', views.DyadDeleteUser, name="update-user"),
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', views.LoginView.as_view(), name='Login'),
    path('user/', views.UserView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('register', views.RegisterView.as_view())
]