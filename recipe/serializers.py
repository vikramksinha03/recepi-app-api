from recipe.models import Recipe
from rest_framework import serializers

class CreateRecipeSerializers(serializers.ModelSerializer):
  """Serializer for Recipe"""

  class Meta:
    model = Recipe
    fields = ['id', 'title', 'time_minute', 'price', 'link']
    read_only_fields = ['id']


class RecipeDetailSerializer(CreateRecipeSerializers):

  class Meta(CreateRecipeSerializers.Meta):
    fields = CreateRecipeSerializers.Meta.fields + ['description']