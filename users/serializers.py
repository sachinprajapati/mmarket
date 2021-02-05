from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = fields = ['phone', 'email', 'name']