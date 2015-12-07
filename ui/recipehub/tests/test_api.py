from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .test_utils import insert_users, insert_recipes, insert_ingredients, get_recipes
from ..utils import set_rating
from ..data import get_recipes_for_users
from pprint import pprint
factory = APIRequestFactory()

class TestCase(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()
        self.john = User.objects.get(username="john")
        self.jane = User.objects.get(username="jane")
        self.jude = User.objects.get(username="jude")
        self.recipes = get_recipes_for_users([self.john.id])
        set_rating(self.recipes[0]['id'], self.jane.id, 3)
        set_rating(self.recipes[1]['id'], self.jude.id, 2)

    def test_top_5(self):
        resp = self.client.get('/api/v1/recipe/?top_five=1').data
        self.assertEqual(len(resp), 2)
