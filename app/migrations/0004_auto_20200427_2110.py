# Generated by Django 2.2.12 on 2020-04-27 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_checkin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='img',
            field=models.ImageField(upload_to='check/'),
        ),
    ]