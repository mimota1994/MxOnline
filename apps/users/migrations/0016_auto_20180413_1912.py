# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-13 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20180413_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='title',
            field=models.CharField(max_length=5, verbose_name='\u6807\u9898'),
        ),
    ]
