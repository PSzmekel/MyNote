from os import stat
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, permission_classes, authentication_classes
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
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated],
                                    'update': [permissions.IsAuthenticated],
                                    'retrieve': [permissions.IsAuthenticated],
                                    'changepass': [permissions.IsAuthenticated]}
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

    def destroy(self, request, *args, **kwargs):
        tokenString = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=tokenString)
        instance = self.get_object()
        if instance.id == token.user.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        tokenString = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=tokenString)
        instance = self.get_object()
        if instance.id != token.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def changepass(self, request, *args, **kwargs):
        user_data = request.data
        tokenString = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=tokenString)
        user = CustomUser.objects.get(id=token.user.id)
        oldPassword = user_data['password_old']
        newPassword = user_data['password']
        if user.check_password(oldPassword):
            user.set_password(newPassword)
            serializer = CustomUserSerializer(
                user, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
