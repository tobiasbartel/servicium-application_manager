# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 09:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0043_auto_20161002_1803'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['name'], 'permissions': (('can_view', 'View project'), ('can_edit', 'Edit project'), ('can_delete', 'Delete project'), ('creator', 'Full access to model features.'))},
        ),
        migrations.AlterModelOptions(
            name='paymentmethod',
            options={'ordering': ['name']},
        ),
    ]
