from django.test import TestCase
from data import (get_recipe, ping, new_recipe, update_recipe, get_recipes_for_users)


class TestPing(TestCase):

    def test_ping(self):
        self.assertIn('pong', ping())

class TestNewRecipe(TestCase):

    def test_new_recipe(self):
        recipe = new_recipe(sunny_side_up['title'], 22, sunny_side_up['ingredients'], sunny_side_up['steps'])
        self.assertEqual(sunny_side_up['title'], recipe['title'])

class TestGetRecipe(TestCase):

    def test_get_recipe(self):
        recipe = new_recipe(sunny_side_up['title'], 22, sunny_side_up['ingredients'], sunny_side_up['steps'])
        recipe_from_server = get_recipe(recipe['id'])
        self.assertEqual(sunny_side_up['title'], recipe_from_server['title'])

class TestUpdateRecipe(TestCase):

    def test_update_recipe(self):
        recipe = new_recipe(sunny_side_up['title'], 22, sunny_side_up['ingredients'], sunny_side_up['steps'])
        updated_recipe = update_recipe(recipe['id'], sunny_side_up_v2['ingredients'], sunny_side_up_v2['steps'])
        self.assertNotEqual(recipe['data']['id'], updated_recipe['data']['id'])

class TestGetRecipesForUsers(TestCase):

    def test_get_recipes_for_users(self):
        user_ids = [22, 23, 24]
        for user_id in user_ids:
            new_recipe(sunny_side_up['title'], user_id, sunny_side_up['ingredients'], sunny_side_up['steps'])
        recipes = get_recipes_for_users(user_ids)
        recipe_users = list(set([recipe['user_id'] for recipe in recipes]))
        self.assertEqual(sorted(user_ids), sorted(recipe_users))


sunny_side_up = {
    # "id": 1,
    "title": "Sunny side up",
    "user_id": 1,
    "fork_of": None,
    "ingredients": {
        "canola_oil": 1,  # one tbsp oil
        "salt": None,     # to taste
        "eggs": 2,        # two eggs
        "hot_sauce": None # to taste
    },
    "steps": [
        "Heat oil in a pan",
        "Break eggs and put them",
        "Add salt and close the lid",
        "Once done serve in plate and put hot sauce"
    ]
}

sunny_side_up_v2 = {
    # "id": 1,
    "title": "Sunny side up",
    "user_id": 1,
    "fork_of": None,
    "ingredients": {
        "canola_oil": 1,  # one tbsp oil
        "salt": None,     # to taste
        "eggs": 2,        # two eggs
        "cheese": 2 # to taste
    },
    "steps": [
        "Heat oil in a pan",
        "Break eggs and put them in the pan",
        "sprinkle cheese on the eggs",
        "Add salt and close the lid",
        "Once done serve in plate"
    ]
}
