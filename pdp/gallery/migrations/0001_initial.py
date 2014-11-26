# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import pdp.gallery.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('subtitle', models.CharField(max_length=200, verbose_name='Sous titre', blank=True)),
                ('slug', models.SlugField(max_length=80)),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update', models.DateTimeField(verbose_name='Date de modification', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Galeries',
                'verbose_name': 'Galerie',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('slug', models.SlugField(max_length=80)),
                ('physical', models.ImageField(upload_to=pdp.gallery.models.image_path)),
                ('legend', models.CharField(max_length=80, verbose_name='Légende')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('update', models.DateTimeField(verbose_name='Date de modification', null=True, blank=True)),
                ('gallery', models.ForeignKey(to='gallery.Gallery', verbose_name='Galerie')),
            ],
            options={
                'verbose_name_plural': 'Images',
                'verbose_name': 'Image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('mode', models.CharField(max_length=1, default='R', choices=[('R', 'Lecture'), ('W', 'Ecriture')])),
                ('gallery', models.ForeignKey(to='gallery.Gallery', verbose_name='Galerie')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Membre')),
            ],
            options={
                'verbose_name_plural': "Galeries de l'utilisateur",
                'verbose_name': "Galeries de l'utilisateur",
            },
            bases=(models.Model,),
        ),
    ]
