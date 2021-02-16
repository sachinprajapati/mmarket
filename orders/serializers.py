from rest_framework import serializers

from .models import *
from admins.models import AvailableAddress
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
    status = serializers.SerializerMethodField('get_Status')
    class Meta:
        model = Orders
        fields = ('id', 'order_id', 'amount', 'status', 'get_payment_type', 'expected_dt', 'dt')

    def get_Status(self, obj):
        return obj.get_Status()

class OrderItemsSerializer(serializers.ModelSerializer):
    product = ListProductSerializer(read_only=True)
    class Meta:
        model = OrderItems
        fields = ("product", "quantity", "price")

class OrderDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    orderitems_set = OrderItemsSerializer(read_only=True, many=True)
    status = serializers.SerializerMethodField('get_Status')
    class Meta:
        model = Orders
        fields = ('id', 'order_id', 'amount', 'status', 'dt', 'address', 'orderitems_set', 'get_payment_type')

    def get_Status(self, obj):
        return obj.get_Status()

class AvailableAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableAddress
        fields = ('pincode', )

class TrackOrder(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('status', 'dt')

class TrackOrderSerializer(serializers.ModelSerializer):
    orderstatus_set = TrackOrder(many=True, read_only=True)
    class Meta:
        model = Orders
        fields = ('order_id', 'amount', 'orderstatus_set')

class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('order', 'status')

    def create(self, validated_data):
        obj = OrderStatus.objects.create(**validated_data)
        for p in obj.order.orderitems_set.all():
            p.product.stockrecord.num_allocated -= p.quantity
            p.product.stockrecord.save()
        return obj
