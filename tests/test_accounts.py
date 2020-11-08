import pytest

from django.db.utils import IntegrityError

from accounts.models import CustomUser


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
