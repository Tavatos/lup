# Generated by Django 4.0.5 on 2022-07-05 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_entity', models.IntegerField()),
                ('entity_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('sector', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('profileimg', models.ImageField(default='blank-profile-picture.png', upload_to='profile_images')),
                ('address', models.CharField(max_length=300)),
                ('contact_no', models.CharField(max_length=200, verbose_name='')),
                ('contact_no2', models.CharField(max_length=200, verbose_name='')),
                ('email_add', models.EmailField(max_length=200)),
                ('postal_add', models.CharField(max_length=200)),
                ('postal_code', models.IntegerField()),
                ('website', models.URLField(verbose_name='')),
                ('location', models.CharField(blank=True, max_length=120)),
                ('province', models.CharField(max_length=200)),
                ('municipality', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
