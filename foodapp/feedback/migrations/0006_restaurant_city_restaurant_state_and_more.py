# Generated by Django 4.2.4 on 2023-10-27 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_review_is_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='city',
            field=models.CharField(default='Charlottesville', max_length=100),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='state',
            field=models.CharField(default='VA', max_length=100),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='street_address',
            field=models.CharField(default="85 Engineer's Way", max_length=100),
        ),
    ]
