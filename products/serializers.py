from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import *


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
	    model = Category
	    fields = ['id', 'name', 'slug', 'img']