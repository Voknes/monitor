# Generated by Django 2.2.12 on 2020-05-26 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200512_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
