from rest_framework import serializers

from .models import *
from products.serializers import ListProductSerializer

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user', )

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ('amount', 'type', 'tid')

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        exclude = ('dt',)

class OrdersListSerializer(serializers.ModelSerializer):
    # status = serializers.SerializerMethodField()
    class Meta:
        model = Orders
        fields = ('id', 'order_id', 'amount', 'status', 'get_payment_type', 'expected_dt', 'dt')

    # def get_status(self, obj):
    #     return obj.get_status_display()

class OrderItemsSerializer(serializers.ModelSerializer):
    product = ListProductSerializer(read_only=True)
    class Meta:
        model = OrderItems
        fields = ("product", "quantity", "price")

class OrderDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    orderitems_set = OrderItemsSerializer(read_only=True, many=True)
    class Meta:
        model = Orders
        fields = ('id', 'order_id', 'amount', 'status', 'dt', 'address', 'orderitems_set', 'get_payment_type')
