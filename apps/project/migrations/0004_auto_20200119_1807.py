# Generated by Django 2.2.7 on 2020-01-19 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20200119_0959'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectSkills',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
