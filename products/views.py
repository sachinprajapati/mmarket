from django.shortcuts import render, get_object_or_404

from rest_framework import permissions, status, viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter

from .models import *
from basket.models import CartLine
from .serializers import *

class CategoryViewSet(generics.ListAPIView):
	model = Category
	queryset = Category.objects.filter(parent=None)
	serializer_class = CategorySerializer
	permission_classes = [permissions.AllowAny]

	def get_queryset(self):
		if self.kwargs.get('parent_id'):
		    parent_id = self.kwargs['parent_id']
		    return self.model.objects.filter(parent_id=parent_id)
		return self.queryset.all()

class ProductFilter(FilterSet):
	min_price = NumberFilter(field_name="price", lookup_expr='gte')
	max_price = NumberFilter(field_name="price", lookup_expr='lte')
	title = CharFilter(lookup_expr='contains')

	class Meta:
		model = Product
		fields = ['categories', 'title', 'price', 'min_price', 'max_price', 'is_discountable']

class ProductViewSet(generics.ListAPIView):
	model = Product
	queryset = Product.objects.filter()
	serializer_class = ListProductSerializer
	permission_classes = [permissions.AllowAny]
	filterset_class = ProductFilter
	filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
	pagination_class = LimitOffsetPagination

class ProductDetailViewSet(generics.RetrieveAPIView):
	model = Product
	serializer_class = DetailProductSerializer
	permission_classes = [permissions.AllowAny]

	def get_object(self):
		if self.kwargs.get('pk'):
			return get_object_or_404(self.model, pk=self.kwargs['pk'])

	def retrieve(self, request, *args, **kwargs):
		product = self.get_object()
		serializer = DetailProductSerializer(product)
		if request.user.is_authenticated:
			response_data = {"cart_count": CartLine.objects.filter(product=product, cart=request.user.cart).count()}
			response_data.update(serializer.data)
			return Response(response_data, status=status.HTTP_200_OK)
		return Response(serializer.data, status=status.HTTP_200_OK)
