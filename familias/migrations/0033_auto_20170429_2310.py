# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-29 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0032_merge_20170429_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='integrante',
            name='especificacion_estudio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='integrante',
            name='especificacion_oficio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='offline_id',
            field=models.TextField(blank=True),
        ),
    ]
