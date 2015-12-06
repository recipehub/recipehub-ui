from django.test import TestCase
from ui.recipehub.models import Ingredient
from ui.recipehub.data import (get_recipe, clean, new_recipe, update_recipe, get_recipes_for_users, fork_recipe)
from django.contrib.auth.models import User


class TestInserts(TestCase):

    def test_inserts(self):
        insert_users()
        insert_ingredients()
        insert_recipes()
        self.assertGreater(User.objects.count(), 0)
        self.assertGreater(Ingredient.objects.count(), 0)
        self.assertGreater(get_recipes_for_users([User.objects.get(username="john").id]), 0)


def insert_ingredients():
    for ingredient  in ingredients:
        Ingredient.objects.create(**ingredient)

def insert_users():
    for user in users:
        User.objects.create_user(*user)

def insert_recipes():
    clean()
    for recipe in get_recipes():
        new_recipe(**recipe)

ingredients = [
    {
        "name": "Butter",
        "unit_of_measurement": "tbsp",
        "fat": 40,
        "carbohydrate": 0,
        "protein": 0,
        "calories": 100
    },
    {
        "name": "Canola Oil",
        "unit_of_measurement": "tbsp",
        "fat": 60,
        "carbohydrate": 2,
        "protein": 0,
        "calories": 120
    },
    {
        "name": "Eggs",
        "unit_of_measurement": "",
        "fat": 20,
        "carbohydrate": 0,
        "protein": 9,
        "calories": 150
    },
    {
        "name": "Pepper",
        "unit_of_measurement": "",
        "fat": 0,
        "carbohydrate": 0,
        "protein": 0,
        "calories": 0
    },
    {
        "name": "Salt",
        "unit_of_measurement": "",
        "fat": 0,
        "carbohydrate": 0,
        "protein": 0,
        "calories": 0
    },
    {
        "name": "Parmesan Cheese",
        "unit_of_measurement": "tbsp",
        "fat": 5,
        "carbohydrate": 1,
        "protein": 3,
        "calories": 25
    },
]

def get_recipes():
    return [
        {
            "title": "Sunny Side up",
            "user_id": User.objects.get(username="john").id,
            "ingredients": {
                Ingredient.objects.get(name="Canola Oil").id: 2,
                Ingredient.objects.get(name="Pepper").id: 0,
                Ingredient.objects.get(name="Salt").id: 0,
                Ingredient.objects.get(name="Eggs").id: 2,
            },
            "steps": [
                "Heat oil in a pan",
                "Break eggs and put them in the pan",
                "sprinkle cheese on the eggs",
                "Add salt and close the lid",
                "Once done serve in plate"
            ]
        }
    ]

users = [
    [
        "john",
        "john@example.com",
        "password"
    ],
    [
        "jane",
        "jane@example.com",
        "password"
    ]
]
