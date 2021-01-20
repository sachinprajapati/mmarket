from django.shortcuts import render, get_object_or_404

from rest_framework import permissions, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from django_filters.rest_framework import CharFilter

from .models import *
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
	name = CharFilter(lookup_expr='contains')

	class Meta:
		model = Product
		fields = ['categories', 'name', 'price', 'min_price', 'max_price']

class ProductViewSet(generics.ListAPIView):
	model = Product
	queryset = Product.objects.filter()
	serializer_class = ListProductSerializer
	permission_classes = [permissions.AllowAny]
	filterset_class = ProductFilter

class ProductDetailViewSet(generics.RetrieveAPIView):
	model = Product
	serializer_class = DetailProductSerializer
	permission_classes = [permissions.AllowAny]

	def get_object(self):
		if self.kwargs.get('pk'):
			return get_object_or_404(self.model, pk=self.kwargs['pk'])
