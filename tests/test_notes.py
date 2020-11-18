import pytest

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser
from notes.models import Note


@pytest.mark.django_db
def test_note_create():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'lennon@thebeatles.com'})
    response = client.post(
        '/api/notes/', {'topic': 'topic2', 'text': 'text2', 'owner': 'lennon@thebeatles.com'})
    assert response.status_code == 201
    assert Note.objects.count() == 2


@pytest.mark.django_db
@pytest.mark.xfail
def test_note_create_bad_mail():
    CustomUser.objects.create_user(
        'bim@thebeatles.com', 'johnpassword')
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'bim@thebeatles.com'})
    assert response.status_code == 403
    assert Note.objects.count() == 0


@pytest.mark.django_db
def test_get():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'lennon@thebeatles.com'})
    response = client.get(
        '/api/notes/')
    assert response.status_code == 200
    assert response != []


@pytest.mark.django_db
@pytest.mark.xfail
def test_get_another_users_note():
    user1 = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token1 = Token.objects.get(user=user1)
    user2 = CustomUser.objects.create_user(
        'lennon1@thebeatles.com', 'johnpassword1')
    token2 = Token.objects.get(user=user2)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)
    client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'lennon@thebeatles.com'})
    noteId = Note.objects.get(topic='topic1').id
    client2 = APIClient()
    client2.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
    response = client2.get(
        '/api/notes/' + noteId + '/')
    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.xfail
def test_delete():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'lennon@thebeatles.com'})
    noteId = Note.objects.get(topic='topic1').id
    response = client.delete(
        '/api/notes/' + noteId + '/')
    assert response.status_code == 200
    assert Note.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.xfail
def test_delete_another_users_note():
    user1 = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token1 = Token.objects.get(user=user1)
    user2 = CustomUser.objects.create_user(
        'lennon1@thebeatles.com', 'johnpassword1')
    token2 = Token.objects.get(user=user2)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)
    client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'lennon@thebeatles.com'})
    noteId = Note.objects.get(topic='topic1').id
    client2 = APIClient()
    client2.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
    response = client2.delete(
        '/api/notes/' + noteId + '/')
    assert response.status_code == 401
    assert Note.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.xfail
def test_note_edit():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'lennon@thebeatles.com'})
    response = client.put(
        '/api/notes/', {'topic': 'topic2', 'text': 'text2'})
    note = Note.objects.get(topic='topic2')
    assert response.status_code == 202
    assert note.created_date != note.last_edit
    assert note.topic == 'topic2'
    assert note.text == 'text2'


@pytest.mark.django_db
@pytest.mark.xfail
def test_note_edit_not_change():
    user = CustomUser.objects.create_user(
        'lennon@thebeatles.com', 'johnpassword')
    token = Token.objects.get(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    client.post(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1', 'owner': 'lennon@thebeatles.com'})
    response = client.put(
        '/api/notes/', {'topic': 'topic1', 'text': 'text1'})
    note = Note.objects.get(topic='topic1')
    assert response.status_code == 202
    assert note.created_date == note.last_edit
