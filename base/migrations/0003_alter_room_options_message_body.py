# Generated by Django 4.0.5 on 2022-06-11 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_topic_room_host_message_room_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-update', '-create']},
        ),
        migrations.AddField(
            model_name='message',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]