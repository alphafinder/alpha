# Generated by Django 2.2.7 on 2020-02-23 14:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('avatar', models.ImageField(blank=True, upload_to='profile/photos/')),
                ('confirmed', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('active_projects_cnt', models.IntegerField(default=0)),
                ('good_teamlead', models.IntegerField(default=0)),
                ('status', models.TextField(default='')),
                ('vk', models.URLField(blank=True, default='', max_length=35)),
                ('linked_in', models.URLField(blank=True, default='', max_length=28)),
                ('telegram', models.URLField(blank=True, default='', max_length=33)),
                ('bio', models.TextField(default='', max_length=80)),
                ('location', models.CharField(default='', max_length=80)),
                ('github_account', models.CharField(default='', max_length=100)),
                ('github_projects_cnt', models.IntegerField(default=0)),
                ('github', models.URLField(blank=True, default='', max_length=38)),
                ('github_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('github_followers', models.IntegerField(default=0)),
                ('github_access_token', models.CharField(blank=True, max_length=40, null=True)),
                ('github_commits', models.IntegerField(default=0)),
                ('github_stars', models.IntegerField(default=0)),
                ('skills', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPasswordRecovery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key1', models.TextField(max_length=64)),
                ('expires', models.DateTimeField(default=datetime.datetime(2020, 2, 24, 14, 30, 13, 136443, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFriendInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancelled', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFriend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmailConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key1', models.TextField(max_length=64)),
                ('key2', models.TextField(max_length=64)),
                ('expires', models.DateTimeField(default=datetime.datetime(2020, 2, 24, 14, 30, 13, 137871, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]