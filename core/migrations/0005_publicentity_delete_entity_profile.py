# Generated by Django 4.0.5 on 2023-05-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_post_remove_entity_profile_id_entity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicEntity',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('entity_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('services', models.TextField(blank=True)),
                ('sector', models.CharField(blank=True, max_length=200, null='True')),
                ('department', models.CharField(blank=True, max_length=200)),
                ('profileimg', models.ImageField(blank=True, default='blank-profile-picture.png', null='True', upload_to='profile_images')),
                ('address', models.CharField(max_length=300)),
                ('contact_no', models.CharField(max_length=200, verbose_name='')),
                ('contact_no2', models.CharField(blank=True, max_length=200, verbose_name='')),
                ('email_add', models.EmailField(max_length=200)),
                ('postal_add', models.CharField(blank=True, max_length=200)),
                ('postal_code', models.IntegerField()),
                ('website', models.URLField(blank=True, verbose_name='')),
                ('location', models.CharField(blank=True, max_length=120)),
                ('municipality', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Entity_Profile',
        ),
    ]
