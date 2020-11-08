from accounts.models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'email']
        extra_kwargs = {'password': {'write_only': True}}
