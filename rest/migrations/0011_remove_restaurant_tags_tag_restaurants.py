# Generated by Django 5.1.3 on 2025-01-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0010_tag_remove_restaurant_tags_restaurant_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='tags',
        ),
        migrations.AddField(
            model_name='tag',
            name='restaurants',
            field=models.ManyToManyField(blank=True, related_name='tags', to='rest.restaurant'),
        ),
    ]
