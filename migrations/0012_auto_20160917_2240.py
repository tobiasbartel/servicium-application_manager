# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0011_module_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmethod',
            name='method',
            field=models.CharField(choices=[('lync', 'Lync'), ('email', 'EMail'), ('phone', 'Office Phone'), ('mobile', 'Mobile Phone'), ('web', 'Web'), ('ocd', 'On Call')], max_length=10),
        ),
    ]
