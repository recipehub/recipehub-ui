from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ingredient, Follow, Rating, Comment

admin.site.register(Ingredient)
admin.site.register(Follow)
admin.site.register(Rating)
admin.site.register(Comment)
