from django.urls import path, include
from rest_framework import routers

from .views import *

# router = routers.DefaultRouter()
# router.register(r'category', CategoryViewSet)


urlpatterns = [
	# path('', include(router.urls)),
    path('category/', CategoryViewSet.as_view()),
    path('category/<int:parent_id>/', CategoryViewSet.as_view()),
    path('products/', ProductViewSet.as_view()),
    path('product/<int:pk>/', ProductDetailViewSet.as_view()),
    path('banner/', BannerListView.as_view()),
    path('discount-products/', ProductDiscountView.as_view()),
    path('dcrg-software/', DCRG)
]