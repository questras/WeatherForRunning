# Generated by Django 2.2.5 on 2019-11-01 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_auto_20191101_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='url',
        ),
    ]
