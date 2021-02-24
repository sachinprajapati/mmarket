from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'wishlist', WishListViewSet)


urlpatterns = [
	path('', include(router.urls)),
    # path('cart/add/', AddTOCart.as_view()),
]