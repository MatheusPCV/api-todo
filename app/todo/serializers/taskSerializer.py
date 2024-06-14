from rest_framework import serializers
from ..models.taskModel import TaskEntity


class TaskSerializer(serializers.Serializer):
    _id = serializers.CharField(allow_blank=True, required=False)
    username = serializers.CharField(allow_blank=True, required=False)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255, allow_blank=True)

    def create(self, validated_data):
        return TaskEntity(**validated_data)
