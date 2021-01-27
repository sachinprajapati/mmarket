from rest_framework import serializers

from .models import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user', )

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        exlcude = ('dt')

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        exclude = ('dt', )

    def validate_empty_values(self, data):
        print(self, data)
