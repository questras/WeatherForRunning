# Generated by Django 2.1.5 on 2019-01-30 15:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_auto_20190130_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
