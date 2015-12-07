from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .test_utils import insert_users, insert_recipes, insert_ingredients, get_recipes
from ..utils import set_rating
from ..data import get_recipes_for_users
from ..models import Comment, Rating
from pprint import pprint
factory = APIRequestFactory()

class TestAPIRecipeList(TestCase):

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


class TestAPIRecipeDetail(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()

    def test_get(self):
        resp = self.client.get('/api/v1/recipe/1/').data
        self.assertEquals(resp['id'], 1)


class TestAPICommentList(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()

    def test_create(self):
        self.client.login(username="jude", password="password")
        resp = self.client.post('/api/v1/comment/', {
            "recipe_id": 1,
            "text": "Test Comment"
        })
        self.assertEquals(Comment.objects.count(), 1)

    def test_get(self):
        self.test_create()
        self.client.logout()
        resp = self.client.get('/api/v1/comment/?recipe_id=1')
        self.assertEquals(len(resp.data), 1)


class TestAPIRating(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()

    def test_set_rating(self):
        self.client.login(username="jude", password="password")
        resp = self.client.post('/api/v1/rating/', {
            "recipe_id": 1,
            "rating": 4
        })
        self.assertEquals(Rating.objects.count(), 1)

    def test_get(self):
        self.test_set_rating()
        self.client.logout()
        resp = self.client.get('/api/v1/recipe/1/')
        self.assertEquals(resp.data['rating'], 4)
