from django.contrib.auth.models import User, Group
from accounts.models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'email', 'groups']
