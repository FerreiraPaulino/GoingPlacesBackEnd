# Generated by Django 5.0.1 on 2024-02-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_car_images_car_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='drivers_license',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
