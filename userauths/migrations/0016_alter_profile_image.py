# Generated by Django 5.1.3 on 2024-12-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0015_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/pink.jpg', upload_to='profile_pics'),
        ),
    ]
