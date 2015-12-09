from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .utils import get_top, get_recipe, set_rating, get_detailed_recipe
from .models import Comment
from .data import get_forks, fork_recipe
from .serializers import RecipeSerializer, CommentSerializer, RatingSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import json
from pprint import pprint


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

@api_view(['GET'])
def current_user(request):
    if not request.user.id:
        return Response({})
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class ForkListCreateView(APIView):
    """
    List all forks of recipe, or create a new fork.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = RecipeSerializer

    def get(self, request, format=None):
        recipe_id = request.GET.get('recipe_id')
        if recipe_id:
            forks = get_forks(recipe_id)
            return Response(json.dumps(forks))

    def post(self, request, format=None):
        recipe_id = request.POST.get('recipe_id')
        if recipe_id:
            fork = fork_recipe(request.user.id, recipe_id)
            serializer = self.serializer_class(data=get_detailed_recipe(fork))
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('', status=status.HTTP_400_BAD_REQUEST)
