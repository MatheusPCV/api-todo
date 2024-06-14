from rest_framework import serializers
from ..models.userModel import UserEntity


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(allow_blank=True, required=False)
    name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        return UserEntity(**validated_data)
