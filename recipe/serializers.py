from recipe.models import Recipe
from rest_framework import serializers
from tags.serializers import TagSerializer
from tags.models import Tag
from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer


class CreateRecipeSerializers(serializers.ModelSerializer):
    """Serializer for Recipe"""

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minute", "price", "link", "tags", "ingredients"]
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags, recipe):
        """Handling getting or creating tags"""
        auth_user = self.context["request"].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handling getting or creating ingredients"""
        auth_user = self.context["request"].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user, **ingredient
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        tags = validated_data.pop(tags, [])
        ingredients = validated_data.pop(ingredients, [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop(tags, None)
        ingredients = validated_data.pop(ingredients, None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(CreateRecipeSerializers):
    class Meta(CreateRecipeSerializers.Meta):
        fields = CreateRecipeSerializers.Meta.fields + ["description"]
