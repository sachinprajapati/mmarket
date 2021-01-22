from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)


urlpatterns = [
	path('', include(router.urls)),
    # path('cart/add/', AddTOCart.as_view()),
]