from rest_framework import serializers

from .models import Seed

class SeedSerializer(serializers.Serializer):
    device_name = serializers.CharField()
    device_type = serializers.CharField()
    device_address = serializers.CharField()
    device_token = serializers.CharField()

    def create(self, validated_data):
        return Seed.objects.create(**validated_data)


