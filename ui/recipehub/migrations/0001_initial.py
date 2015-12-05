# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipe_id', models.BigIntegerField(db_index=True)),
                ('text', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follower', models.ForeignKey(related_name='follower_of_user', to=settings.AUTH_USER_MODEL)),
                ('follows', models.ForeignKey(related_name='user_followed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, db_index=True)),
                ('unit_of_measurement', models.CharField(max_length=10)),
                ('fat', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('carbohydrate', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('protein', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('calories', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipe_id', models.BigIntegerField(db_index=True)),
                ('rating', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
