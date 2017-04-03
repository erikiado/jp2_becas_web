# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-21 17:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0010_auto_20170315_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrante',
            name='apellidos',
            field=models.CharField(default='López', max_length=200),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='fecha_de_nacimiento',
            field=models.DateField(default='1996-02-26'),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='nivel_estudios',
            field=models.CharField(choices=[('ninguno', 'Ninguno'), ('1_grado', 'Primero de Primaria'), ('2_grado', 'Segundo de Primaria'), ('3_grado', 'Tercero de Primaria'), ('4_grado', 'Cuarto de Primaria'), ('5_grado', 'Quinto de Primaria'), ('6_grado', 'Sexto de Primaria'), ('7_grado', 'Primero de Secundaria'), ('8_grado', 'Segundo de Secundaria'), ('9_grado', 'Tercero de Secundaria'), ('10_grado', 'Primero de Pecundaria'), ('11_grado', 'Segundo de Preparatoria'), ('12_grado', 'Tercero de Preparatoria'), ('universidad', 'Universidad'), ('maestria', 'Maestría'), ('doctorado', 'Doctorado')], max_length=200),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='nombres',
            field=models.CharField(default='Javier', max_length=200),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='telefono',
            field=models.TextField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "+999999999" Up to 15 numbers allowed', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]