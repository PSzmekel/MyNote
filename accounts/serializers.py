from accounts.models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'email', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = CustomUser(
                email=validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
