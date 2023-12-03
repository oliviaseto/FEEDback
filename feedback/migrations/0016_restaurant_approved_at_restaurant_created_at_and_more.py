# Generated by Django 4.2.5 on 2023-12-01 10:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0015_alter_restaurant_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='review',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]