# Generated by Django 2.2.12 on 2020-05-03 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200503_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='longitude',
        ),
    ]
