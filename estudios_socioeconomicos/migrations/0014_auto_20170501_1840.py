# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-01 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estudios_socioeconomicos', '0013_auto_20170408_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='eleccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estudios_socioeconomicos.OpcionRespuesta'),
        ),
    ]
