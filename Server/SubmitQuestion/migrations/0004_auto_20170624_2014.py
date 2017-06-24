# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SubmitQuestion', '0003_auto_20170624_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitbooleanquestion',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User'),
        ),
        migrations.AlterField(
            model_name='submitmultiplequestion',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User'),
        ),
    ]
