from django.db import models
from django.contrib.auth.models import User
from .models import Ingredient, Follow, Rating, Comment

def get_followers(user_id):
    followers = Follow.objects.filter(follows=user_id)
    return [record.follower for record in followers ]
    
def get_following(user_id):
    followers = Follow.objects.filter(follower=user_id)
    return [record.follows for record in followers ]
    
def get_all_comments(recipe_id):
    return Comment.objects.filter(recipe_id=recipe_id).order_by('timestamp')