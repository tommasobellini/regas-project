# Generated by Django 2.2.1 on 2019-05-25 05:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0009_auto_20190525_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='max_value',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='min_value',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='sensorline',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 25, 5, 45, 7, 990074)),
        ),
    ]
