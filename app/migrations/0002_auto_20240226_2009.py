# Generated by Django 2.2.28 on 2024-02-26 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture_url',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]