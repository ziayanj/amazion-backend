from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
import pytest

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
