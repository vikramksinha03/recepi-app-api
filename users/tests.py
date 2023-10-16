from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.

"""
Test for creating users
"""
class ModelTest(TestCase):
  def test_user_create_with_email(self):
    email = 'test@example.com'
    password = 'testpass123'
    name = 'test'
    user = get_user_model().objects.create_user(
      email=email,
      password=password,
      name = name
    )
    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))


"""
Tests for the user api
"""
CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')

def create_user(**params):
  """Create a new user"""
  return get_user_model().objects.create_user(**params)

class PublicUserTestApi(TestCase):
  """Test unauthenticated API for users who are not yet registerd"""

  def setUp(self):
    self.client = APIClient()

  def test_create_user_success(self):
    """Test creating a user successful"""
    payload = {
      'email': 'test@example.com',
      'password': 'testpass123',
      'name': 'Test Name',
    }
    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(email=payload['email'])
    self.assertEqual(user.password, payload['password'])
    # self.assertNotIn('password', res.data)

  def test_user_email_exist_error(self):
    """Test user with existing email returns error"""
    payload = {
      'email': 'test@example.com',
      'password': 'testpass123',
      'name': 'Test Name'
    }
    create_user(**payload)
    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_password_too_short(self):
    """Test if the the password is too short"""
    payload = {
      'email': 'test@example.com',
      'password': 'pw',
      'name': 'Test Name',
    }
    res = self.client.post('CREATE_USER_URL', payload)
    self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    user_exists = get_user_model().objects.filter(email=payload['email']).exists()
    self.assertFalse(user_exists)

  def test_create_token_for_user(self):
    """Create creating token for a valid credentials"""
    user_detail = {
      'email': 'test@example.com',
      'password': 'test-user-password123',
      'name': 'Test Name'
    }
    create_user(**user_detail)

    payload = {
      'email': user_detail['email'],
      'password': user_detail['password']
    }
    res = self.client.post(TOKEN_URL, payload)
    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)


  def test_create_token_bad_creadential(self):
    """Test return error if the creadential provided is invalid"""
    # user_detail ={
    #   'email': 'test@example.com', 
    #   'password': 'goodpass123'
    # }
    # create_user(**user_detail)
    payload = {
      'email': 'test@example.com', 'password': 'badpass123'
    }

    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_blank_password(self):
    payload ={
      'email': 'test@example.com',
      'password': ''
    }
    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  
  def test_retrieve_user_unauthorized(self):
    res = self.client.get(reverse('users:me'))
    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivetUserApiTest(TestCase):
  """Test API request that requires authentication"""
  def setUp(self):
    self.user = create_user(
      email = 'test@example.com',
      password = 'testpass123',
      name = 'Test Name',
    )
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

  def test_retrieve_profile_success(self):
    """Test retrieving profile for logged in users"""
    res = self.client.get(reverse('users:me'))
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, {
      'email': self.user.email,
      'password': self.user.password,
      'name': self.user.name,
    })

  def test_post_me_not_allowed(self):
    """Test post method not allowed for the me endpoint"""
    res = self.client.post(reverse('users:me'), {})
    self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  def test_update_user_profile(self):
    """Test updating user profile for authenticated user"""
    payload = {
      'name': 'Update Name',
      'password': 'newtestpass123',
    }
    res = self.client.patch(reverse('users:me'), payload)
    self.user.refresh_from_db()
    self.assertEqual(self.user.name, payload['name'])
    self.assertEqual(self.user.password, payload['password'])
    self.assertEqual(res.status_code, status.HTTP_200_OK)