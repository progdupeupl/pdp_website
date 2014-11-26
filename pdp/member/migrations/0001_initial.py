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
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('token', models.CharField(blank=True, max_length=40, verbose_name='Clé')),
                ('expires', models.DateTimeField(default=datetime.date(2014, 11, 26), verbose_name='Expiration de la clé')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name_plural': 'Demandes d’inscription',
                'verbose_name': 'Demande d’inscription',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForgotPasswordToken',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('token', models.CharField(blank=True, max_length=40, verbose_name='Clé')),
                ('expires', models.DateTimeField(default=datetime.date(2014, 11, 26), verbose_name='Expiration de la clé')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name_plural': 'Demandes réinitialisation mot de passe',
                'verbose_name': 'Demande réinitialisation mot de passe',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('site', models.CharField(blank=True, max_length=128, verbose_name='Site internet')),
                ('show_email', models.BooleanField(default=True, verbose_name='Afficher adresse mail publiquement')),
                ('avatar_url', models.CharField(null=True, blank=True, max_length=128, verbose_name='URL de l’avatar')),
                ('biography', models.TextField(blank=True, verbose_name='Biographie')),
                ('mail_on_private_message', models.BooleanField(default=True, verbose_name='Mail messages privé')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur', unique=True)),
            ],
            options={
                'verbose_name_plural': 'Profils',
                'verbose_name': 'Profil',
            },
            bases=(models.Model,),
        ),
    ]
