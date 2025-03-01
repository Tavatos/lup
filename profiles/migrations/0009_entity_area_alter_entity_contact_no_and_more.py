# Generated by Django 4.0.5 on 2023-07-28 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_entity_lat_entity_lon'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='area',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='entity',
            name='contact_no',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='entity',
            name='contact_no2',
            field=models.CharField(blank=True, max_length=20, verbose_name='contact 2'),
        ),
    ]
