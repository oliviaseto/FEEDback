# Generated by Django 4.2.4 on 2023-10-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_review_not_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
