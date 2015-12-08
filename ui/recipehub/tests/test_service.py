from django.test import TestCase
from ui.recipehub.data import (get_recipe, ping, new_recipe, update_recipe, get_recipes_for_users, fork_recipe, get_forks, get_versions, get_recipe_version)


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

class TestForkRecipe(TestCase):

    def test_fork_recipe(self):
        recipe = new_recipe(sunny_side_up['title'], 22, sunny_side_up['ingredients'], sunny_side_up['steps'])
        forked_recipe = fork_recipe(22, recipe['id'])
        self.assertNotEqual(recipe['id'], forked_recipe['id'])
        self.assertEqual(recipe['data']['id'], forked_recipe['data']['id'])
        self.assertEqual(recipe['id'], forked_recipe['fork_of_id'])

class TestForkList(TestCase):

    def test_fork_list(self):
        recipe = new_recipe(sunny_side_up['title'], 22, sunny_side_up['ingredients'], sunny_side_up['steps'])
        forked_recipe = fork_recipe(22, recipe['id'])
        self.assertEqual(len(get_forks(recipe['id'])), 1)

class TestVersionList(TestCase):

    def test_version_list(self):
        recipe = new_recipe(sunny_side_up['title'], 22, sunny_side_up['ingredients'], sunny_side_up['steps'])
        updated_recipe = update_recipe(recipe['id'], sunny_side_up_v2['ingredients'], sunny_side_up_v2['steps'])
        self.assertEqual(len(get_versions(recipe['id'])), 2)
        self.assertIn(recipe['data']['id'], get_versions(recipe['id']))
        self.assertIn(recipe['data']['id'], get_versions(updated_recipe['id']))

class TestRecipeVersion(TestCase):

    def test_recipe_version(self):
        recipe = new_recipe(sunny_side_up['title'], 22, sunny_side_up['ingredients'], sunny_side_up['steps'])
        updated_recipe = update_recipe(recipe['id'], sunny_side_up_v2['ingredients'], sunny_side_up_v2['steps'])
        old_version = get_recipe_version(updated_recipe['id'], recipe['data']['id'])
        self.assertNotIn("cheese", old_version['data']['ingredients'])

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
