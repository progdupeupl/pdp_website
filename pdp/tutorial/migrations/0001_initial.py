# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pdp.tutorial.models
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to=pdp.tutorial.models.image_path, null=True, blank=True)),
                ('thumbnail', models.ImageField(upload_to=pdp.tutorial.models.image_path, null=True, blank=True)),
                ('position_in_part', models.IntegerField(verbose_name='Position dans la partie', null=True, blank=True)),
                ('position_in_tutorial', models.IntegerField(verbose_name='Position dans le tutoriel', null=True, blank=True)),
                ('title', models.CharField(max_length=80, verbose_name='Titre', blank=True)),
                ('introduction', models.TextField(verbose_name='Introduction', blank=True)),
                ('conclusion', models.TextField(verbose_name='Conclusion', blank=True)),
                ('slug', models.SlugField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Chapitres',
                'verbose_name': 'Chapitre',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extract',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('position_in_chapter', models.IntegerField(verbose_name='Position dans le chapitre')),
                ('text', models.TextField(verbose_name='Texte')),
                ('chapter', models.ForeignKey(to='tutorial.Chapter', verbose_name='Chapitre parent')),
            ],
            options={
                'verbose_name_plural': 'Extraits',
                'verbose_name': 'Extrait',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position_in_tutorial', models.IntegerField(verbose_name='Position dans le tutoriel', null=True, blank=True)),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('introduction', models.TextField(verbose_name='Introduction', blank=True)),
                ('conclusion', models.TextField(verbose_name='Conclusion', blank=True)),
                ('slug', models.SlugField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Parties',
                'verbose_name': 'Partie',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('image', models.ImageField(upload_to=pdp.tutorial.models.image_path, default=None, null=True, blank=True)),
                ('thumbnail', models.ImageField(upload_to=pdp.tutorial.models.thumbnail_path, default=None, null=True, blank=True)),
                ('introduction', models.TextField(verbose_name='Introduction', null=True, blank=True)),
                ('conclusion', models.TextField(verbose_name='Conclusion', null=True, blank=True)),
                ('slug', models.SlugField(max_length=80)),
                ('pubdate', models.DateTimeField(verbose_name='Date de publication', blank=True)),
                ('update', models.DateTimeField(verbose_name='Date d’édition', null=True, blank=True)),
                ('size', models.CharField(max_length=1, default='B', verbose_name='Taille du tutoriel', choices=[('S', 'Mini'), ('M', 'Standard'), ('B', 'Étendu')])),
                ('is_visible', models.BooleanField(default=False, verbose_name='Est visible publiquement')),
                ('is_pending', models.BooleanField(default=False, verbose_name='Est en attente')),
                ('is_beta', models.BooleanField(default=False, verbose_name='Est en bêta')),
                ('is_article', models.BooleanField(default=False, verbose_name='Est un article')),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Auteurs')),
            ],
            options={
                'verbose_name_plural': 'Tutoriels',
                'verbose_name': 'Tutoriel',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TutorialCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('slug', models.SlugField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Catégories de tutoriel',
                'verbose_name': 'Catégorie de tutoriel',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='category',
            field=models.ForeignKey(to='tutorial.TutorialCategory', verbose_name='Catégorie', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tutorial',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', help_text='A comma-separated list of tags.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='part',
            name='tutorial',
            field=models.ForeignKey(to='tutorial.Tutorial', verbose_name='Tutoriel parent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='part',
            field=models.ForeignKey(to='tutorial.Part', verbose_name='Partie parente', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='tutorial',
            field=models.ForeignKey(to='tutorial.Tutorial', verbose_name='Tutoriel parent', null=True, blank=True),
            preserve_default=True,
        ),
    ]
