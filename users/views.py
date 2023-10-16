"""
Views for user API
"""
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics, authentication, permissions


class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
  serializer_class = AuthTokenSerializer
  renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
  """Manage the authenticated user"""
  serializer_class = UserSerializer
  authentication_class = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    return self.request.user