# Generated by Django 3.1.7 on 2021-03-28 00:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20210327_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_due',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 30, 0, 0, 46, 66555), verbose_name='Date Due'),
        ),
    ]
