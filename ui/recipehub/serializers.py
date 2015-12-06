from rest_framework import serializers

class RecipeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    rating = serializers.FloatField()
    user = serializers.JSONField()
    ingredients = serializers.JSONField()
    nutrition = serializers.JSONField()
    steps = serializers.JSONField()
