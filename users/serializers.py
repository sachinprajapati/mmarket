from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    refer = serializers.CharField(max_length=10, allow_null=True, allow_blank=True)
    class Meta:
        model = User
        fields = ['phone', 'email', 'name', 'refer']

    def validate(self, attrs):
        if attrs.get('parent'):
            print("in if", attrs)
            try:
                attrs['parent'] = User.objects.get(phone=attrs['refer'])
                attrs.pop("refer")
            except Exception as e:
                raise serializers.ValidationError({"refer": e})
        return attrs

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = fields = ['phone', 'email', 'name']