# Generated by Django 4.2.4 on 2023-10-28 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0008_alter_restaurant_lat_alter_restaurant_lng'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='lng',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='street_address',
            field=models.CharField(max_length=100),
        ),
    ]
