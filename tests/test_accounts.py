import pytest

from django.db.utils import IntegrityError
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

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

# API


@pytest.mark.django_db
def test_get_users():
    CustomUser.objects.create_user('lennon@thebeatles.com', 'johnpassword')
    client = APIClient()
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert response.data != []


@pytest.mark.django_db
def test_post_user():
    client = APIClient()
    response = client.post(
        '/api/users/', {'email': 'test@mail.com', 'password': 'password'})
    assert response.status_code == 201
    assert CustomUser.objects.count() == 1


@pytest.mark.django_db
def test_post_user_uniqe():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    client = APIClient()
    response = client.post(
        '/api/users/', {'email': 'lennon@thebeatles.com', 'password': 'johnpassword'})
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_user_bad1():
    client = APIClient()
    response = client.post(
        '/api/users/', {'email': 'test@mail.com'})
    assert response.status_code == 400
    assert CustomUser.objects.count() == 0


@pytest.mark.django_db
def test_post_user_bad2():
    client = APIClient()
    response = client.post(
        '/api/users/', {'password': 'password'})
    assert response.status_code == 400
    assert CustomUser.objects.count() == 0


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
    assert user.check_password('johnpassword') == True


@pytest.mark.django_db
def test_delete_user():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    client = APIClient()
    response = client.delete('/api/users/' + str(user.id) + '/')
    assert response.status_code == 204
    assert CustomUser.objects.count() == 0


@pytest.mark.django_db
def test_auto_token():
    client = APIClient()
    response = client.post(
        '/api/users/', {'email': 'test@mail.com', 'password': 'password'})
    assert response.status_code == 201
    assert Token.objects.count() == 1
