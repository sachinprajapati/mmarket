from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Wallet, WalletHistory

class UserCreateSerializer(serializers.ModelSerializer):
    refer = serializers.CharField(max_length=10, allow_null=True, allow_blank=True, write_only=True, required=False)
    class Meta:
        model = User
        fields = ['phone', 'email', 'name', 'refer']

    def validate(self, attrs):
        if attrs.get('refer'):
            try:
                attrs['parent'] = User.objects.get(phone=attrs['refer'])
                attrs.pop("refer")
            except Exception as e:
                raise serializers.ValidationError({"refer": e})
        return attrs

# class WalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = ('bal',)

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['phone', 'email', 'name', 'balance']


class UserDownlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'name', 'children', 'parent_id']

class WalletLogs(serializers.ModelSerializer):
    class Meta:
        model = WalletHistory
        fields = ("prev_bal", "amount", "dt")
