# Generated by Django 5.1.3 on 2024-12-31 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0008_alter_restaurant_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, default='restaurant_images/default-rest.png', null=True, upload_to='restaurant_images'),
        ),
    ]