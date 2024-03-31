# Generated by Django 5.0.1 on 2024-02-08 10:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_car_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_added',
        ),
        migrations.AddField(
            model_name='customuser',
            name='ratings',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]
