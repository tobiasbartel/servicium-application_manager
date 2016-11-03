# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 10:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact_manager', '0007_auto_20161020_0758'),
        ('servicecatalog', '0051_auto_20161020_1037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modulecontact',
            old_name='module',
            new_name='parent',
        ),
        migrations.AlterUniqueTogether(
            name='modulecontact',
            unique_together=set([('parent', 'contact', 'role')]),
        ),
    ]