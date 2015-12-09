from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .test_utils import insert_users, insert_recipes, insert_ingredients, get_recipes, get_updated_recipe
from ..utils import set_rating
from ..data import get_recipes_for_users, fork_recipe, clean
from ..models import Comment, Rating
from pprint import pprint
import json
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


class TestAPIRecipeCreate(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        clean()
        self.john = User.objects.get(username="john")
        self.jane = User.objects.get(username="jane")
        self.jude = User.objects.get(username="jude")

    def test_create(self):
        self.client.login(username="john", password="password")
        self.client.post('/api/v1/recipe/', data=json.dumps(get_recipes()[0]), content_type="application/json")
        self.assertEqual(len(self.client.get('/api/v1/recipe/?user_id={}'.format(self.john.id)).data), 1)

class TestAPIRecipeDetail(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()

    def test_get(self):
        resp = self.client.get('/api/v1/recipe/1/').data
        self.assertEquals(resp['id'], 1)


class TestAPIRecipeVersion(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()

    def test_get(self):
        self.client.login(username="john", password="password")
        self.client.put('/api/v1/recipe/{}/'.format(1), data=json.dumps(get_updated_recipe()),
                                    content_type="application/json")
        resp = json.loads(self.client.get('/api/v1/version/{}/'.format(1)).data)
        self.assertEqual(len(resp), 2)

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

class TestAPIUser(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()
        self.jude = User.objects.get(username="jude")

    def test_logged_in_user(self):
        self.client.login(username=self.jude.username, password="password")
        resp = self.client.get('/api/v1/user/')
        self.assertEqual(resp.data['id'], self.jude.id)

    def test_guest_user(self):
        resp = self.client.get('/api/v1/user/')
        self.assertEqual(resp.data, {})

class TestAPIForks(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()
        self.jude = User.objects.get(username="jude")

    def test_fork(self):
        self.client.login(username=self.jude.username, password="password")
        resp = self.client.post('/api/v1/fork/', {
            'recipe_id': 1
        })
        self.assertEqual(resp.data['fork_of_id'], 1)

    def test_list_forks(self):
        self.test_fork()
        resp = self.client.get('/api/v1/fork/', {
            'recipe_id': 1
        })
        self.assertEqual(len(json.loads(resp.data)), 1)

class TestAPIForks(TestCase):

    def setUp(self):
        insert_users()
        insert_ingredients()
        insert_recipes()
        self.jude = User.objects.get(username="jude")

    def test_fork(self):
        self.client.login(username=self.jude.username, password="password")
        resp = self.client.post('/api/v1/fork/', {
            'recipe_id': 1
        })
        self.assertEqual(resp.data['fork_of_id'], 1)

    def test_list_forks(self):
        self.test_fork()
        resp = self.client.get('/api/v1/fork/', {
            'recipe_id': 1
        })
        self.assertEqual(len(json.loads(resp.data)), 1)
