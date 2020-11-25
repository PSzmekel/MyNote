from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from notes.serializers import NoteSerializer
from notes.models import Note
from accounts.models import CustomUser


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Note.objects.all().order_by('created_date')
    serializer_class = NoteSerializer
    permission_classes_by_action = {'create': [permissions.IsAuthenticated],
                                    'list': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated],
                                    'update': [permissions.IsAuthenticated],
                                    'retrieve': [permissions.IsAuthenticated]}
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        tokenString = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=tokenString)
        notes = Note.objects.filter(owner=token.user.email)
        return notes

    def create(self, request, *args, **kwargs):
        user_data = request.data
        tokenString = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=tokenString)
        user = CustomUser.objects.get(
            is_staff=False, is_active=True, id=token.user.id)
        if user.email == user_data['owner']:
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except MultiValueDictKeyError as e:
                content = {'Value is required': str(e)}
                return Response(content, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            content = {'Invalid mail': 'owner mail is not for user'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
