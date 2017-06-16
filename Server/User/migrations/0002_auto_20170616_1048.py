# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 02:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='My Domain <noreply@mydomain.com>', max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='0', max_length=11),
        ),
    ]
