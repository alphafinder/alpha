# Generated by Django 2.2.7 on 2019-12-24 16:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20191222_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremailconfirmation',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 25, 16, 58, 27, 569472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpasswordrecovery',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 25, 16, 58, 27, 569472, tzinfo=utc)),
        ),
    ]
