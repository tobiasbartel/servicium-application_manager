# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0036_auto_20161002_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulewritestomodule',
            name='payment_methods',
            field=models.ManyToManyField(blank=True, default=None, to='servicecatalog.PaymentMethod'),
        ),
    ]
