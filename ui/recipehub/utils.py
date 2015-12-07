from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Ingredient, Follow, Rating, Comment
from .data import get_recipe as _get_recipe
from pprint import pprint
from copy import deepcopy


def get_followers(user_id):
    followers = Follow.objects.filter(follows=user_id)
    return [record.follower for record in followers]

def get_following(user_id):
    followers = Follow.objects.filter(follower=user_id)
    return [record.follows for record in followers]

def get_ingredient_list(ingredient_dict):
    return [(Ingredient.objects.get(pk=key), ingredient_dict[key]) for key in ingredient_dict]

def get_detailed_ingredients(ingredients):
    ret = []
    ingredient_tuple_list = get_ingredient_list(ingredients)
    for ingredient in ingredient_tuple_list:
        ret.append({'id':ingredient[0].id, 'name':ingredient[0].name, 'amount':ingredient[1], 'unit_of_measurement':ingredient[0].unit_of_measurement})
    return ret

def get_rating(recipe_id):
    ret = Rating.objects.filter(recipe_id=recipe_id).values("recipe_id").annotate(average = Avg("rating"))
    if ret:
        return ret[0]['average']

def set_rating(recipe_id, user_id, rating):
    if not rating >= 0 or not rating <=5:
        raise RatingException
    if get_recipe(recipe_id)['user_id'] == user_id:
        raise RatingException
    rating_obj = Rating.objects.filter(recipe_id=recipe_id, user_id=user_id).first()
    if not rating_obj:
        rating_obj = Rating(recipe_id=recipe_id, user_id=user_id)
    rating_obj.rating = rating
    rating_obj.save()

def get_top(number=5):
    top = Rating.get_top(number)
    return [get_recipe(x['recipe_id']) for x in top]


class RatingException(Exception):
    pass

def get_detailed_nutrition(ingredients):
    nutrition_dict = {"fat" : 0, "carbohydrate" : 0, "protein" : 0, "calories" : 0}
    ingredients_tuple_list = get_ingredient_list(ingredients)
    for ingredient in ingredients_tuple_list:
        for key in nutrition_dict:
            nutrition_dict[key] += (getattr(ingredient[0],key) * ingredient[1])
    return nutrition_dict

def get_recipe(recipe_id):
    return get_detailed_recipe(_get_recipe(recipe_id))

def get_user_dict(user_id):
    user = User.objects.get(pk=user_id)
    return {
        "username": user.username,
        "id": user_id,
        "email": user.email
    }

def get_detailed_recipe(recipe):
    recipe = deepcopy(recipe)
    recipe.update(recipe['data'])
    del recipe['data']
    # pprint(recipe)
    recipe['nutrition'] = get_detailed_nutrition(recipe['ingredients'])
    recipe['ingredients'] = get_detailed_ingredients(recipe['ingredients'])
    recipe['rating'] = get_rating(recipe['id'])
    recipe['user'] = get_user_dict(recipe['user_id'])
    return recipe
