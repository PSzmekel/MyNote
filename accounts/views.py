from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, status
from accounts.serializers import CustomUserSerializer
from accounts.models import CustomUser
from rest_framework.response import Response


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = CustomUser.objects.filter(is_staff=False, is_active=True)
        return users

    def create(self, request, *args, **kwargs):
        user_data = request.data
        try:
            user = CustomUser.objects.create_user(
                email=user_data['email'], password=user_data['password'])
        except MultiValueDictKeyError as e:
            content = {'Value is required': str(e)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        serializer = CustomUserSerializer(
            user, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
