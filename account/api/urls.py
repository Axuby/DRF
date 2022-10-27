from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.api.serializers import LoginSerializer

from . import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('login/', obtain_auth_token, name='login'), // DRF Token Login
    # path('login/', views.CustomLoginToken.as_view(serializer_class=LoginSerializer), name='login'),
    path('register/', views.reqistration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
