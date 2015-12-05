import requests
import json
from django.conf import settings

def get_recipe(recipe_id):
     r = requests.get(settings.RECIPEHUB_MS_URL + '/recipe/{}'.format(recipe_id))
     r.raise_for_status()
     return r.json()

def new_recipe(title, user_id, ingredients, steps):
    r = requests.post(settings.RECIPEHUB_MS_URL + '/recipe/', data=json.dumps({
        'title': title,
        'user_id': user_id,
        'ingredients': ingredients,
        'steps': steps
    }))
    r.raise_for_status()
    return r.json()

def update_recipe(recipe_id, ingredients, steps):
    r = requests.put(settings.RECIPEHUB_MS_URL + '/recipe/{}/'.format(recipe_id), data=json.dumps({
        'recipe_id': recipe_id,
        'ingredients': ingredients,
        'steps': steps
    }))
    r.raise_for_status()
    return r.json()

def get_recipes_for_users(user_ids):
     r = requests.get(settings.RECIPEHUB_MS_URL + '/recipe/', data={
         'user_id': user_ids
     })
     r.raise_for_status()
     return r.json()

def fork_recipe(user_id, recipe_id):
    print user_id
    r = requests.post(settings.RECIPEHUB_MS_URL + '/fork/{}/'.format(recipe_id), data=json.dumps({
        'user_id': user_id,
    }))
    r.raise_for_status()
    return r.json()

def ping():
    return requests.get(settings.RECIPEHUB_MS_URL + '/ping').json()
