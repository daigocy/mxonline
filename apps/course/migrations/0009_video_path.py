# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-19 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20170719_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='path',
            field=models.CharField(default='', max_length=100, verbose_name='\u8def\u5f84'),
        ),
    ]