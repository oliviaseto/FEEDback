# Generated by Django 4.2.4 on 2023-11-01 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0009_alter_restaurant_city_alter_restaurant_lat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]