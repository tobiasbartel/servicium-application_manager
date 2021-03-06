# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 09:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact_manager', '0007_auto_20161020_0758'),
        ('servicecatalog', '0047_auto_20161018_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleContacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicecatalog.Contact')),
                ('contact_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact_manager.ContactRole')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicecatalog.Module')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='modulecontacts',
            unique_together=set([('module', 'contact', 'contact_role')]),
        ),
    ]
