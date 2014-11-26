# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('position', models.IntegerField(verbose_name='Position', null=True, blank=True)),
                ('slug', models.SlugField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Catégories',
                'verbose_name': 'Catégorie',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('subtitle', models.CharField(max_length=200, verbose_name='Sous-titre', blank=True)),
                ('position_in_category', models.IntegerField(verbose_name='Position dans la catégorie', null=True, blank=True)),
                ('slug', models.SlugField(max_length=80)),
                ('category', models.ForeignKey(to='forum.Category', verbose_name='Catégorie')),
            ],
            options={
                'verbose_name_plural': 'Forums',
                'verbose_name': 'Forum',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Texte')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Date de publication')),
                ('update', models.DateTimeField(verbose_name="Date d'édition", null=True, blank=True)),
                ('position_in_topic', models.IntegerField(verbose_name='Position dans le sujet')),
                ('is_useful', models.BooleanField(default=False, verbose_name='Est utile')),
                ('is_moderated', models.BooleanField(default=False, verbose_name='Est modéré')),
                ('moderation_time', models.DateTimeField(default=datetime.datetime(2014, 11, 26, 20, 15, 36, 701382), verbose_name="Date d'édition")),
                ('moderation_text', models.TextField(default='', verbose_name='Explication de modération', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur', related_name='posts')),
                ('moderated_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Modérateur', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('subtitle', models.CharField(max_length=200, verbose_name='Sous-titre', blank=True)),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('is_solved', models.BooleanField(default=False, verbose_name='Est résolu')),
                ('is_locked', models.BooleanField(default=False, verbose_name='Est verrouillé')),
                ('is_sticky', models.BooleanField(default=False, verbose_name='Est en post-it')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur', related_name='topics')),
                ('forum', models.ForeignKey(to='forum.Forum', verbose_name='Forum')),
                ('last_message', models.ForeignKey(to='forum.Post', verbose_name='Dernier message', related_name='last_message', null=True)),
            ],
            options={
                'verbose_name_plural': 'Sujets',
                'verbose_name': 'Sujet',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicFollowed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('topic', models.ForeignKey(to='forum.Topic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='topics_followed')),
            ],
            options={
                'verbose_name_plural': 'Sujets suivis',
                'verbose_name': 'Sujet suivi',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicRead',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('post', models.ForeignKey(to='forum.Post')),
                ('topic', models.ForeignKey(to='forum.Topic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='topics_read')),
            ],
            options={
                'verbose_name_plural': 'Sujets lus',
                'verbose_name': 'Sujet lu',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(to='forum.Topic', verbose_name='Sujet'),
            preserve_default=True,
        ),
    ]
