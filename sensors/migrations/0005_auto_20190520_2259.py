# Generated by Django 2.2.1 on 2019-05-20 22:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0004_auto_20190520_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorline',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 20, 22, 59, 36, 149594)),
        ),
        migrations.AlterField(
            model_name='sensorline',
            name='humidity',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='sensorline',
            name='temperature',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
