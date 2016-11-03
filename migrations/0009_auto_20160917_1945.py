# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0008_auto_20160917_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmethod',
            name='method',
            field=models.CharField(choices=[('lync', 'Lync'), ('email', 'EMail'), ('phone', 'Office Phone'), ('mobile', 'Mobile Phone'), ('web', 'Web')], max_length=10),
        ),
        migrations.AlterField(
            model_name='instance',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instance_to_module', to='servicecatalog.Module'),
        ),
    ]
