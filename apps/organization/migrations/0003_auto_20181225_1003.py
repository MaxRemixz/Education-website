# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-25 02:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20181224_0001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='catgory',
            new_name='category',
        ),
    ]
