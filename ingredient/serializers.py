from rest_framework import serializers
from ingredient.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient"""

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]
