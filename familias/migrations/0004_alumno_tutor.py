# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-23 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0003_merge_20170223_0525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True)),
                ('integrante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='familias.Integrante')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relacion', models.TextField(choices=[('madre', 'Madre'), ('padre', 'Padre'), ('tutor', 'Tutor')])),
                ('integrante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='familias.Integrante')),
            ],
        ),
    ]
