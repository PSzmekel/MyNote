from accounts.models import CustomUser
from rest_framework import serializers
from notes.serializers import NoteMiniSerializer


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    notes = NoteMiniSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'email', 'notes']
        extra_kwargs = {'password': {'write_only': True}}
