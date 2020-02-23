# Generated by Django 2.2.7 on 2020-02-23 14:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200223_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremailconfirmation',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 14, 36, 40, 983449, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpasswordrecovery',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 14, 36, 40, 981975, tzinfo=utc)),
        ),
    ]
