from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_top, get_recipe, set_rating
from .models import Comment
from .serializers import RecipeSerializer, CommentSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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

class RecipeDetailView(APIView):

    def get(self, request, recipe_id=1):
        recipe = get_recipe(recipe_id)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)


class CommentListCreateView(APIView):
    """
    List all comments, or create a new comment.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get(self, request, format=None):
        comments = []
        recipe_id = request.GET.get('recipe_id')
        if recipe_id:
            comments = Comment.objects.filter(recipe_id=recipe_id).order_by('timestamp')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            Comment.objects.create(user_id=request.user.id, **serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingCreateView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request, format=None):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            set_rating(serializer.data['recipe_id'], request.user.id, serializer.data['rating'])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
