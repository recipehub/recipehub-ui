from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .utils import get_top, get_recipe, set_rating, get_detailed_recipe
from .models import Comment, RecipeImage, Ingredient
from .data import get_forks, fork_recipe, update_recipe, get_versions, new_recipe, get_recipes_for_users
from .serializers import RecipeSerializer, CommentSerializer, RatingSerializer, UserSerializer, RecipeImageSerializer, IngredientSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import json
from pprint import pprint
from base64 import b64decode
from django.core.files.base import ContentFile
from .cluster_utils import search_recipies


class RecipeListCreateView(APIView):
    """
    List all recipes, or create a new recipe.
    """
    serializer_class = RecipeSerializer
    def get(self, request, format=None):
        recipes = []
        if request.GET.get('top_five'):
            recipes = get_top(5)
        if request.GET.get('user_id'):
            recipes = get_recipes_for_users([request.GET.get('user_id')])
            recipes = [get_detailed_recipe(recipe) for recipe in recipes]
        serializer = self.serializer_class(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            recipe = new_recipe(serializer.data['title'], serializer.data['description'], request.user.id, serializer.data['ingredients'], serializer.data['steps'])
            return Response(get_detailed_recipe(recipe), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeDetailView(APIView):
    serializer_class = RecipeSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, recipe_id):
        version_id = request.GET.get('version_id')
        recipe = get_recipe(recipe_id, version_id=version_id)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, recipe_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            update_recipe(recipe_id, serializer.data['ingredients'], serializer.data['steps'], description=serializer.data.get('description'), message=serializer.data.get('message'), title=serializer.data.get('title'))
            return Response('', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(['GET'])
def search(request):
    q = request.GET.get('q')
    if q:
        return Response(json.dumps(search_recipies(q)))
    return Response(status=status.HTTP_400_BAD_REQUEST)


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
            forks = [get_detailed_recipe(recipe) for recipe in forks]
            return Response(json.dumps(forks))

    def post(self, request, format=None):
        recipe_id = request.data.get('recipe_id')
        if recipe_id:
            fork = fork_recipe(request.user.id, recipe_id)
            serializer = self.serializer_class(data=get_detailed_recipe(fork))
            serializer.is_valid()
            ret = dict(serializer.data)
            ret['id'] = int(fork['id'])
            return Response(ret, status=status.HTTP_201_CREATED)
        return Response('', status=status.HTTP_400_BAD_REQUEST)

class VersionListView(APIView):
    """
    List versions
    """
    serializer = RecipeSerializer
    def get(self, request, recipe_id, format=None):
        return Response(json.dumps(get_versions(recipe_id)))

class IngredientListView(APIView):
    """
    List ingredients
    """
    serializer_class = IngredientSerializer
    def get(self, request, format=None):
        data = Ingredient.objects.all()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)


class RecipeImageGetCreateView(APIView):
    serializer_class = RecipeImageSerializer

    def get(self, request, format=None):
        recipe_id = request.GET.get('recipe_id')
        print 'here', recipe_id
        if recipe_id:
            image = RecipeImage.objects.get(recipe_id=recipe_id)
            res = self.serializer_class(image)
            return Response(res.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if request.data.get('image') and request.data.get('recipe_id'):
            data = {
                'recipe_id': request.data.get('recipe_id'),
                'image': ContentFile(request.data.get('image'), 'testimg.png')
            }
            image = RecipeImage.objects.create(**data)
            print image.file
            res = self.serializer_class(image)
            return Response(res.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
