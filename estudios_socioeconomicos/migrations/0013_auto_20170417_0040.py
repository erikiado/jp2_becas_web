# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-17 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudios_socioeconomicos', '0012_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='file_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='foto',
            name='upload',
            field=models.ImageField(upload_to=''),
        ),
    ]
