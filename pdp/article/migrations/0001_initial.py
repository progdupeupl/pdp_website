# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import pdp.article.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('text', models.TextField(verbose_name='Texte', blank=True)),
                ('slug', models.SlugField(max_length=80)),
                ('pubdate', models.DateTimeField(verbose_name='Date de publication', blank=True)),
                ('image', models.ImageField(upload_to=pdp.article.models.image_path, default=None, null=True, blank=True)),
                ('thumbnail', models.ImageField(upload_to=pdp.article.models.thumbnail_path, default=None, null=True, blank=True)),
                ('is_visible', models.BooleanField(default=False, verbose_name='Est visible publiquement')),
                ('is_pending', models.BooleanField(default=False, verbose_name='Est en attente')),
                ('is_beta', models.BooleanField(default=False, verbose_name='Est visible par les membres')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur', related_name='articles')),
            ],
            options={
                'verbose_name_plural': 'Articles',
                'verbose_name': 'Article',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('slug', models.SlugField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Catégories d’article',
                'verbose_name': 'Catégorie d’article',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='article.ArticleCategory', verbose_name='Catégorie', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', help_text='A comma-separated list of tags.'),
            preserve_default=True,
        ),
    ]
