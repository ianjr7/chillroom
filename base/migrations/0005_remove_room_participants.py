# Generated by Django 4.0.5 on 2022-06-12 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='participants',
        ),
    ]
