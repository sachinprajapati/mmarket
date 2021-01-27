from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'address', AddressView)


urlpatterns = [
	path('', include(router.urls)),
	path('checkout/', CheckOutView.as_view())
    # path('cart/add/', AddTOCart.as_view()),
]