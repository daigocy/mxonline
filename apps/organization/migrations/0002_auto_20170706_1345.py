# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-06 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='description',
            field=models.TextField(max_length=200, verbose_name='\u63cf\u8ff0'),
        ),
    ]
