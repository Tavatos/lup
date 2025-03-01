# Generated by Django 4.0.5 on 2023-05-30 06:57

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_reveiw_curator_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.IntegerField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='entity_profile',
            name='id_entity',
        ),
        migrations.RemoveField(
            model_name='entity_profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user_profile',
            name='id',
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='contact_no2',
            field=models.CharField(blank=True, max_length=200, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='department',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='postal_add',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='postal_code',
            field=models.IntegerField(max_length=7),
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='profileimg',
            field=models.ImageField(blank=True, default='blank-profile-picture.png', null='True', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='sector',
            field=models.CharField(blank=True, max_length=200, null='True'),
        ),
        migrations.AlterField(
            model_name='entity_profile',
            name='website',
            field=models.URLField(blank=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='forum',
            name='id',
            field=models.IntegerField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reveiw',
            name='comment',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='reveiw',
            name='id',
            field=models.IntegerField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='id_user',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
