from rest_framework import serializers

class RecipeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    rating = serializers.FloatField()
    fork_of_id = serializers.IntegerField()
    user = serializers.JSONField()
    id = serializers.IntegerField()
    ingredients = serializers.JSONField()
    nutrition = serializers.JSONField()
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
