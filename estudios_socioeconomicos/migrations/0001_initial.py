# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-25 02:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfiles_usuario', '0001_initial'),
        ('familias', '0005_auto_20170225_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado'), ('borrador', 'Borrador'), ('revision', 'Revisión'), ('eliminado', 'Eliminado')])),
                ('numero_sae', models.TextField(blank=True)),
                ('capturista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perfiles_usuario.Capturista')),
                ('familia', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='familias.Familia')),
            ],
        ),
        migrations.CreateModel(
            name='OpcionRespuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('relacionado_a_integrante', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.TextField(blank=True)),
                ('estudio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudios_socioeconomicos.Estudio')),
                ('integrante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='familias.Integrante')),
                ('opcion', models.ManyToManyField(blank=True, null=True, to='estudios_socioeconomicos.OpcionRespuesta')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudios_socioeconomicos.Pregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('numero', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='pregunta',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudios_socioeconomicos.Seccion'),
        ),
        migrations.AddField(
            model_name='opcionrespuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudios_socioeconomicos.Pregunta'),
        ),
    ]