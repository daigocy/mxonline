# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-13 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20170707_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=50, verbose_name='\u7c7b\u522b'),
            preserve_default=False,
        ),
    ]
