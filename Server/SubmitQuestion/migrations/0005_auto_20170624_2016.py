# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SubmitQuestion', '0004_auto_20170624_2014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submitbooleanquestion',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='submitmultiplequestion',
            old_name='userId',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='submitbooleanquestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User'),
        ),
        migrations.AlterField(
            model_name='submitmultiplequestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User'),
        ),
    ]