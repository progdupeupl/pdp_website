# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivatePost',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('text', models.TextField(verbose_name='Texte')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Date de publication')),
                ('update', models.DateTimeField(null=True, blank=True, verbose_name="Date d'édition")),
                ('position_in_topic', models.IntegerField(verbose_name='Position dans le sujet')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur', related_name='privateposts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrivateTopic',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=80, verbose_name='Titre')),
                ('subtitle', models.CharField(blank=True, max_length=200, verbose_name='Sous-titre')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur', related_name='author')),
                ('last_message', models.ForeignKey(null=True, to='privatemessages.PrivatePost', verbose_name='Dernier message', blank=True, related_name='last_message')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='participants', verbose_name='Participants')),
            ],
            options={
                'verbose_name_plural': 'Messages privés',
                'verbose_name': 'Message privé',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrivateTopicRead',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('privatepost', models.ForeignKey(to='privatemessages.PrivatePost')),
                ('privatetopic', models.ForeignKey(to='privatemessages.PrivateTopic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='privatetopics_read')),
            ],
            options={
                'verbose_name_plural': 'Messages privés lus',
                'verbose_name': 'Message privé lu',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='privatepost',
            name='privatetopic',
            field=models.ForeignKey(to='privatemessages.PrivateTopic', verbose_name='Message privé'),
            preserve_default=True,
        ),
    ]
