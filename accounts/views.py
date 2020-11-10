from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from accounts.serializers import CustomUserSerializer
from accounts.models import CustomUser
from rest_framework.response import Response


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        tokenString = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=tokenString)
        users = CustomUser.objects.filter(
            is_staff=False, is_active=True, id=token.user.id)
        return users

    def create(self, request, *args, **kwargs):
        user_data = request.data
        try:
            user = CustomUser.objects.create_user(
                email=user_data['email'], password=user_data['password'])
        except MultiValueDictKeyError as e:
            content = {'Value is required': str(e)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            content = {'Value error': 'email exists in system'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        serializer = CustomUserSerializer(
            user, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
