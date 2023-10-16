from django.shortcuts import render
from rest_framework import viewsets
from recipe.serializers import CreateRecipeSerializers, RecipeDetailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe.models import Recipe

# Create your views here.


class RecipeViewSet(viewsets.ModelViewSet):
    """View to manage recipe APIs"""

    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipe for authenticated users"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return CreateRecipeSerializers
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        return serializer.save(user=self.request.user)
