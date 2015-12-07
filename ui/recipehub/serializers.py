from rest_framework import serializers

class RecipeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    rating = serializers.FloatField()
    user = serializers.JSONField()
    id = serializers.IntegerField()
    ingredients = serializers.JSONField()
    nutrition = serializers.JSONField()
    steps = serializers.JSONField()

class CommentSerializer(serializers.Serializer):
    user = serializers.JSONField()
    id = serializers.IntegerField()
    recipe_id = serializers.IntegerField()
    text = serializers.TextField()
    timestamp = serializers.DateTimeField()
