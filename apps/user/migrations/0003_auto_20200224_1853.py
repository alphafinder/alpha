# Generated by Django 2.2.7 on 2020-02-24 18:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200224_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremailconfirmation',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 25, 18, 53, 38, 225312, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpasswordrecovery',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 25, 18, 53, 38, 223866, tzinfo=utc)),
        ),
    ]
