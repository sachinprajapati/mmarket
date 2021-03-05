from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import *
from admins.models import Banner

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
	    model = Category
	    fields = ['id', 'name', 'slug', 'img']

class ProductAttributeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductAttribute
		fields = ('name', 'code', 'set_value')

class ProductAttributeValueSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductAttributeValue
		exclude = ('id', 'product')

class ProductValueSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductAttributeValue
		fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ('id', 'img')

class ListProductSerializer(serializers.ModelSerializer):
	first_image = serializers.URLField()
	class Meta:
	    model = Product
	    fields = ('id', 'name', 'mrp', 'price', 'first_image', 'is_discountable')

class DetailProductSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(read_only=True, many=True)
	categories = CategorySerializer(read_only=True, many=True)
	# attributes = ProductAttributeSerializer(read_only=True, many=True)
	attributes = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()
	stockrecord = serializers.SerializerMethodField()

	def get_description(self, instance):
		from django.utils.html import strip_tags
		return strip_tags(instance.description)

	def get_stockrecord(self, instance):
		if hasattr(instance, 'stockrecord'):
			if instance.stockrecord.num_in_stock-instance.stockrecord.num_allocated>0:
				return True
		return False

	def get_attributes(self, instance):
		ls = []
		for i in instance.attributes.all():
			value = ProductAttributeValue.objects.get(attribute=i, product=self.instance)
			ls.append({'name': i.name, 'code': i.code, 'value': getattr(value, 'value_'+i.type)})
		return ls

	class Meta:
	    model = Product
	    fields = ('id', 'name', 'images', 'mrp', 'price', 'description', 'categories', 'rating', 'stockrecord','date_created', 'attributes')

class ListBannerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Banner
		fields = "__all__"