# Generated by Django 4.2.7 on 2023-11-15 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentorclub', '0009_user_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='fields',
            new_name='field',
        ),
    ]