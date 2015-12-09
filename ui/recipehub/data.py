import requests
import json
from django.conf import settings

def get_recipe(recipe_id):
    return request('get', '/recipe/{}'.format(recipe_id))

def new_recipe(title, description, user_id, ingredients, steps):
    return request('post', '/recipe/', {
         'title': title,
         'user_id': user_id,
         'ingredients': ingredients,
         'description': description,
         'steps': steps
    })

def update_recipe(recipe_id, ingredients, steps, message=None, title=None, description=None):
    return request('put', '/recipe/{}/'.format(recipe_id), {
         'recipe_id': recipe_id,
         'ingredients': ingredients,
         'steps': steps,
         'title': title,
         'description': description,
         'message': message
    })

def get_recipes_for_users(user_ids):
    return request('get', '/recipe/', {
         'user_id': user_ids
    })

def fork_recipe(user_id, recipe_id):
    return request('post', '/fork/{}/'.format(recipe_id), {
         'user_id': user_id
    })

def get_forks(recipe_id):
    return request('get', '/fork/'.format(recipe_id), {
         'recipe_id': recipe_id,
    })

def get_versions(recipe_id):
    return request('get', '/version/{}'.format(recipe_id))

def get_recipe_version(recipe_id, version_id):
    return request('get', '/recipe/{}/'.format(recipe_id), {
         'version_id': version_id
    })

def ping():
    return request('get', '/ping')

def clean():
    return requests.get(settings.RECIPEHUB_MS_URL + '/clean')

def request(request_type, path, data={}):
    path = settings.RECIPEHUB_MS_URL + path
    if request_type == "get":
        if not isinstance(data, str):
            r = requests.get(path, params=data)
    elif request_type == "post" or request_type == "put":
        data = json.dumps(data)
        r = getattr(requests, request_type)(path, data=data)
        r.raise_for_status()
    return r.json()

