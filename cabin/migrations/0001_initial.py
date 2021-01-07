# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=70, unique=True)),
                ('phone', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('object_id', models.PositiveIntegerField(default=None)),
                ('content_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_type', models.CharField(choices=[('A', 'class A'), ('B', 'class B'), ('C', 'class C')], max_length=3)),
                ('model', models.IntegerField()),
                ('color', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_time', models.IntegerField()),
                ('dropoff_time', models.IntegerField()),
                ('rider_rating', models.FloatField()),
                ('driver_rating', models.FloatField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabin.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('car_type', models.CharField(choices=[('A', 'class A'), ('B', 'class B'), ('C', 'class C')], max_length=3)),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabin.Rider')),
            ],
        ),
        migrations.AddField(
            model_name='ride',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cabin.RideRequest'),
        ),
        migrations.AddField(
            model_name='payment',
            name='ride',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabin.Ride'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabin.Driver'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
