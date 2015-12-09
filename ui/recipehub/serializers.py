from rest_framework import serializers
from .models import RecipeImage
from drf_extra_fields.fields import Base64ImageField

class RecipeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200, required=False)
    message = serializers.CharField(max_length=200, required=False)
    rating = serializers.FloatField(read_only=True)
    fork_of_id = serializers.IntegerField(required=False)
    user = serializers.JSONField(required=False)
    id = serializers.IntegerField(read_only=True)
    ingredients = serializers.JSONField()
    nutrition = serializers.JSONField(required=False)
    steps = serializers.JSONField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()


class CommentSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)
    recipe_id = serializers.IntegerField()
    text = serializers.CharField()
    timestamp = serializers.DateTimeField(read_only=True)


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    recipe_id = serializers.IntegerField()

class RecipeImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    recipe_id = serializers.IntegerField()

    class Meta:
        model = RecipeImage
