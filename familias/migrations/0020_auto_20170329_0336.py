# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-29 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0019_auto_20170329_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrante',
            name='nivel_estudios',
            field=models.CharField(choices=[('ninguno', 'Ninguno'), ('1_grado', 'Primero de Primaria'), ('2_grado', 'Segundo de Primaria'), ('3_grado', 'Tercero de Primaria'), ('4_grado', 'Cuarto de Primaria'), ('5_grado', 'Quinto de Primaria'), ('6_grado', 'Sexto de Primaria'), ('7_grado', 'Primero de Secundaria'), ('8_grado', 'Segundo de Secundaria'), ('9_grado', 'Tercero de Secundaria'), ('10_grado', 'Primero de Pecundaria'), ('11_grado', 'Segundo de Preparatoria'), ('12_grado', 'Tercero de Preparatoria'), ('universidad', 'Universidad'), ('maestria', 'Maestría'), ('doctorado', 'Doctorado')], max_length=200),
        ),
    ]
