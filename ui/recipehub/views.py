from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_top
from .serializers import RecipeSerializer


class RecipeListCreateView(APIView):
    """
    List all recipes, or create a new recipe.
    """
    def get(self, request, format=None):
        recipes = []
        if request.GET.get('top_five'):
            recipes = get_top(5)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
