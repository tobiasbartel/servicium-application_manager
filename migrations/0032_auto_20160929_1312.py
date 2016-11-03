# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0031_auto_20160928_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='image',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]