from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator

# Ingredient model
# includes name and unit of measurement and nutrition info
class Ingredient(models.Model):

    name = models.CharField(max_length=50, db_index=True)
    unit_of_measurement = models.CharField(max_length=10)
    fat = models.FloatField(validators = [MinValueValidator(0.0)])
    carbohydrate = models.FloatField(validators = [MinValueValidator(0.0)])
    protein = models.FloatField(validators = [MinValueValidator(0.0)])
    calories = models.FloatField(validators = [MinValueValidator(0.0)])

    def __unicode__(self):
        return unicode(self.name)

# Follow model
# User follows another user
# follows is a single user followed by the User
class Follow(models.Model):

    follower = models.ForeignKey(User, db_index=True, related_name='follower_of_user')
    follows = models.ForeignKey(User, related_name='user_followed')

    def __unicode__(self):
        return unicode(self.follower) + u' Follows ' + unicode(self.follows)


# Rating model
# recipe_id is a recipe id which fetchs Recipe from RecipeMicroservie
# Group by recipe_id and averaging on rating gives average rating of a particular recipe
class Rating(models.Model):

    recipe_id = models.BigIntegerField(db_index=True)
    user = models.ForeignKey(User)
    rating = models.IntegerField()

    def __unicode__(self):
        return u'recipe:' + unicode(self.recipe_id) + u' user:' + unicode(self.user) + u' rating:' + unicode(self.rating)

    @classmethod
    def get_top(self,number):
        return Rating.objects.values("recipe_id").annotate(rating=Avg("rating")).order_by('-rating')[:number]

class Comment(models.Model):

    recipe_id = models.BigIntegerField(db_index=True)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'recipe:' + unicode(self.recipe_id) + u' text:' + unicode(self.text) + u' ' + unicode(self.timestamp)


class RecipeImage(models.Model):

    recipe_id = models.BigIntegerField(db_index=True)
    image = models.ImageField()
