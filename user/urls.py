from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView,ChangePasswordView, UserProfileView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-view'),
    path('change_passwrod/', ChangePasswordView.as_view(), name='change-password'),
    path('user_profile/', UserProfileView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='login_obtain_pair'),
    path('login/refresh/',TokenRefreshView.as_view(), name='login_refresh'),
]
