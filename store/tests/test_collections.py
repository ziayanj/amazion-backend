from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from store.models import Collection

@pytest.fixture
def create_collection(api_client):
  def do_create_collection(collection):
    return api_client.post('/store/collections/', collection)
  
  return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
  # @pytest.mark.skip
  def test_if_user_is_anonymous_returns_401(self, create_collection):
    # client = APIClient()
    # response = api_client.post('/store/collections/', { 'title': 'a' })
    response = create_collection({ 'title': 'a' })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
    # client = APIClient()
    # api_client.force_authenticate(user={})
    # response = api_client.post('/store/collections/', { 'title': 'a' })
    authenticate()

    response = create_collection({ 'title': 'a' })

    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_data_is_invalid_returns_400(self, create_collection, authenticate):
    # client = APIClient()
    # api_client.force_authenticate(user=User(is_staff=True))
    # response = api_client.post('/store/collections/', { 'title': '' })
    authenticate(is_staff=True)

    response = create_collection({ 'title': '' })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None

  def test_if_data_is_valid_returns_201(self, create_collection, authenticate):
    # client = APIClient()
    # api_client.force_authenticate(user=User(is_staff=True))
    # response = api_client.post('/store/collections/', { 'title': 'a' })
    authenticate(is_staff=True)
 
    response = create_collection({ 'title': 'a' })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
  def test_if_collection_exists_returns_200(self, api_client):
    collection = baker.make(Collection)

    response = api_client.get(f'/store/collections/{collection.id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
      'id': collection.id,
      'title': collection.title,
      'products_count': 0
    }

  def test_if_collection_does_not_exist_returns_404(self, api_client):
    response = api_client.get('/store/collections/-1/')

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestUpdateCollection:
  def test_if_collection_updates_returns_200(self, api_client, authenticate):
    collection = baker.make(Collection)
    authenticate(is_staff=True)

    response = api_client.patch(f'/store/collections/{collection.id}/', { 'title': 'a' })

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'a'

  def test_if_collection_does_not_exist_returns_404(self, api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.patch('/store/collections/-1/', { 'title': 'a' })

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestListCollection:
  def test_if_collection_list_returns_200(self, api_client):
    collection = baker.make(Collection)

    response = api_client.get('/store/collections/')

    assert response.status_code == status.HTTP_200_OK
    assert any(obj == {
      'id': collection.id,
      'title': collection.title,
      'products_count': 0
    } for obj in response.data)

  def test_if_no_collection_returns_200(self, api_client):
    response = api_client.get('/store/collections/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []

@pytest.mark.django_db
class TestDestroyCollection:
  def test_if_user_is_anonymmous_returns_401(self, api_client):
    collection = baker.make(Collection)

    response = api_client.delete(f'/store/collections/{collection.id}/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, api_client, authenticate):
    authenticate()
    collection = baker.make(Collection)

    response = api_client.delete(f'/store/collections/{collection.id}/')

    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_collection_does_not_exist_returns_404(self, api_client, authenticate):
    authenticate(is_staff=True)

    response = api_client.delete('/store/collections/-1/')

    assert response.status_code == status.HTTP_404_NOT_FOUND


  def test_if_collection_deleted_returns_204(self, api_client, authenticate):
    authenticate(is_staff=True)
    collection = baker.make(Collection)

    response = api_client.delete(f'/store/collections/{collection.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
