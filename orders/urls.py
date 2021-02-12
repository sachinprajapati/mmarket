from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'address', AddressView)
router.register(r'orders', OrdersView)


urlpatterns = [
	path('', include(router.urls)),
	path('checkout/', CheckOutView.as_view()),
	path('track-order/<int:pk>/', TrackOrder.as_view()),
	path('pincode-available/<int:pincode>/', PincodeAvailView.as_view())
	# path('orders/', OrdersView.as_view()),
    # path('cart/add/', AddTOCart.as_view()),
]