# Generated by Django 4.2.4 on 2023-11-12 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0013_alter_restaurant_admin_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='zip_code',
            field=models.IntegerField(default=22903, max_length=5),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]