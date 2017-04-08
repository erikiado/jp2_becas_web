# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-06 21:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicadores', '0002_auto_20170224_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingreso',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutor_ingresos', to='familias.Tutor'),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='familia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacciones', to='familias.Familia'),
        ),
    ]
