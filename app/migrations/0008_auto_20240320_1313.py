# Generated by Django 2.2.28 on 2024-03-20 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20240319_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date_time',
            field=models.DateTimeField(),
        ),
    ]