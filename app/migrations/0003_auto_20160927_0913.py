# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-27 09:13
from __future__ import unicode_literals

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160922_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='image',
            field=models.ImageField(null=True, upload_to=app.models.PathAndRename('img/initiative_events/')),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='title_pt',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]