from django.conf.urls import url
from django.urls import path
from core import views
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenObtainPairView

urlpatterns = [
    #url(r'^core/users$', views.user_list),
    # path('test-ping/', views.test_ping),
    path('users-list/', views.DyadGetAllUsers, name="users-list"),
    path('create-user/', views.DyadCreateUser, name="create-user"),
    path('update-user/<str:pk>', views.DyadUpdateUserFields, name="update-user"),
    path('delete-user/<str:pk>', views.DyadDeleteUser, name="update-user")
 #   path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
 #   path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')    
]