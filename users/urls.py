from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('sign-up/', UserViewSet.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('send-otp/', SendOTP.as_view()),
    path('profile/', ProfileView.as_view()),
    path('downlines/', Downlines.as_view())
]