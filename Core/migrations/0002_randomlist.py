# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-08 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomList',
            fields=[
                ('random_list_number', models.AutoField(primary_key=True, serialize=False)),
                ('site_name', models.TextField(default=None, null=True)),
                ('site_description', models.TextField(default=None, null=True)),
                ('page_url', models.TextField(default=None, null=True)),
            ],
        ),
    ]
