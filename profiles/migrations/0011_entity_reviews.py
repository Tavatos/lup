# Generated by Django 4.0.5 on 2023-07-31 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0007_alter_review_rating'),
        ('profiles', '0010_alter_entity_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='reviews',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entity_reviews', to='review.review'),
        ),
    ]
