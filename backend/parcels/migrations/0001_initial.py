# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CadastralBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('file', models.FileField(max_length=500, upload_to='uploads/cadastral_blocks', verbose_name='file')),
                ('original_file_name', models.CharField(max_length=100, verbose_name='original file name')),
                ('original_file_size', models.PositiveIntegerField(verbose_name='original file size')),
                ('cadastral_number', models.CharField(blank=True, max_length=40, null=True, verbose_name='cadastral number')),
            ],
            options={
                'ordering': ('-modified',),
                'verbose_name_plural': 'Cadastral Blocks',
                'verbose_name': 'Cadastral Block',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('cadastral_number', models.CharField(max_length=40, verbose_name='cadastral number')),
                ('utilization', models.CharField(max_length=200, verbose_name='utilization')),
                ('path_json', models.TextField(verbose_name='path JSON')),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parcels', to='parcels.CadastralBlock', verbose_name='block')),
            ],
            options={
                'ordering': ('-modified',),
                'verbose_name_plural': 'Parcels',
                'verbose_name': 'Parcel',
                'abstract': False,
            },
        ),
    ]
