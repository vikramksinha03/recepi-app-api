from recipe.models import Recipe
from rest_framework import serializers
from tags.serializers import TagSerializer
from tags.models import Tag


class CreateRecipeSerializers(serializers.ModelSerializer):
    """Serializer for Recipe"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minute", "price", "link", "tags"]
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags, recipe):
        auth_user = self.context["request"].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        tags = validated_data.pop(tags, [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop(tags, None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(CreateRecipeSerializers):
    class Meta(CreateRecipeSerializers.Meta):
        fields = CreateRecipeSerializers.Meta.fields + ["description"]
