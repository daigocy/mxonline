# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-08 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20170707_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=26, verbose_name='\u5e74\u9f84'),
        ),
    ]
