# Generated by Django 4.2.4 on 2023-11-11 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0012_restaurant_admin_message_restaurant_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='admin_message',
            field=models.TextField(blank=True, default=''),
        ),
    ]
