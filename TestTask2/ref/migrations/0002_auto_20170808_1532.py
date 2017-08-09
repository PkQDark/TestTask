# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-08 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ref', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referaluser',
            options={'ordering': ['-point']},
        ),
        migrations.AlterField(
            model_name='referalnumber',
            name='numbers',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='referaluser',
            name='referal',
            field=models.EmailField(blank=True, max_length=225, null=True),
        ),
    ]