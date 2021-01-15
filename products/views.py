from django.shortcuts import render, get_object_or_404

from rest_framework import permissions, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *

class CategoryViewSet(generics.ListAPIView):
	model = Category
	queryset = Category.objects.filter(parent=None)
	serializer_class = CategorySerializer
	permission_classes = [permissions.AllowAny]

	# def get_permissions(self):
	# 	permission_classes = []
	# 	if self.action == 'list' or self.action == 'retrieve':
	# 	    permission_classes = [permissions.AllowAny]
	# 	else:
	# 	    permission_classes = [permissions.IsAdminUser]
	# 	return [permission() for permission in permission_classes]

	def get_queryset(self):
		if self.kwargs.get('parent_id'):
		    parent_id = self.kwargs['parent_id']
		    return self.model.objects.filter(parent_id=parent_id)
		return self.queryset.all()
