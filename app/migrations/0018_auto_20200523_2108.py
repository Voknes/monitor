# Generated by Django 2.2.12 on 2020-05-23 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_tarifs'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.RemoveField(
            model_name='checkin',
            name='img',
        ),
    ]