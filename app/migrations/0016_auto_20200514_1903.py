# Generated by Django 2.2.12 on 2020-05-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200513_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='rout',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reports',
            name='tv',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]