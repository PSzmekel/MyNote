import pytest

from django.db.utils import IntegrityError
from rest_framework.test import APIClient

from accounts.models import CustomUser

# User


@pytest.mark.django_db
def test_user_create():
    CustomUser.objects.create_user('lennon@thebeatles.com', 'johnpassword')
    CustomUser.objects.create_user('lennon1@thebeatles.com', 'johnpassword')
    assert CustomUser.objects.count() == 2


@pytest.mark.django_db
def test_user_create_unique():
    is_unique = True
    try:
        CustomUser.objects.create_user('lennon@thebeatles.com', 'johnpassword')
        CustomUser.objects.create_user('lennon@thebeatles.com', 'johnpassword')
    except(IntegrityError):
        is_unique = False
    assert is_unique == False


@pytest.mark.django_db
def test_user_create_pass_ok():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    assert user.check_password('johnpassword')


@pytest.mark.django_db
def test_user_create_pass_not_ok():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    assert user.check_password('johnpassworda') == False

# Super User


@pytest.mark.django_db
def test_superuser_create():
    superuser = CustomUser.objects.create_superuser(
        'lennon@thebeatles.com', 'johnpassword')
    superuser2 = CustomUser.objects.create_superuser(
        'lennon2@thebeatles.com', 'johnpassword')
    assert superuser.is_staff == True and superuser2.is_staff == True


@pytest.mark.django_db
def test_superuser_create_unique():
    is_unique = True
    try:
        superuser = CustomUser.objects.create_superuser(
            'lennon@thebeatles.com', 'johnpassword')
        superuser2 = CustomUser.objects.create_superuser(
            'lennon@thebeatles.com', 'johnpassword')
    except(IntegrityError):
        is_unique = False
    assert is_unique == False

# API


@pytest.mark.django_db
def test_get_users():
    CustomUser.objects.create_user('lennon@thebeatles.com', 'johnpassword')
    client = APIClient()
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert response.data != []


@pytest.mark.django_db
def test_get_superuser():
    CustomUser.objects.create_superuser(
        'lennon@thebeatles.com', 'johnpassword')
    client = APIClient()
    response = client.get('/api/users/')
    assert response.data == []  # can't get superuser by api, dataset shoudl be empty


@pytest.mark.django_db
def test_post_user():
    client = APIClient()
    response = client.post(
        '/api/users/', {'email': 'test@mail.com', 'password': 'password'})
    assert response.status_code == 201
    assert CustomUser.objects.count() == 1


@pytest.mark.django_db
def test_put_user():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    client = APIClient()
    response = client.put(
        '/api/users/' + str(user.id) + '/', {'email': 'test1@mail.com', 'password': 'password1'})
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.email == 'test1@mail.com'


@pytest.mark.django_db
def test_delete_user():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    client = APIClient()
    response = client.delete('/api/users/' + str(user.id) + '/')
    assert response.status_code == 204
    assert CustomUser.objects.count() == 0
