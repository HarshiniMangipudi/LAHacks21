# Generated by Django 3.1.7 on 2021-03-28 00:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20210328_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_due',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 30, 0, 2, 27, 256005), verbose_name='Date Due'),
        ),
    ]
