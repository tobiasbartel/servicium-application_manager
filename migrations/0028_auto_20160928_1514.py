# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0027_module_connected_to_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='modulewritestomodule',
            name='payment_methods',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='servicecatalog.PaymentMethod'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='state',
            field=models.CharField(choices=[('d', 'In development'), ('l', 'Live'), ('X', 'Depricated')], default='l', max_length=1),
        ),
    ]
