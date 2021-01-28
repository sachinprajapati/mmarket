from rest_framework import serializers

from .models import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user', )

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        exclude = ('dt',)

class GetOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"
