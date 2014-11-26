# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='to_tutorial',
            field=models.ForeignKey(to='tutorial.Tutorial', verbose_name='Tutoriel correspondant', null=True, blank=True),
            preserve_default=True,
        ),
    ]
