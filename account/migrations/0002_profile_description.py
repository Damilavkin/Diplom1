# Generated by Django 5.1 on 2024-08-20 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Description',
            field=models.TextField(default='Нет описания'),
        ),
    ]
