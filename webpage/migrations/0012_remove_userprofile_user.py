# Generated by Django 4.2.1 on 2023-12-01 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0011_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
    ]
