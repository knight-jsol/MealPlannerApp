# Generated by Django 4.2.1 on 2023-11-17 01:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0003_alter_pantryitem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pantryitem',
            old_name='item_amount',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='pantryitem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='pantryitem',
            name='user',
        ),
        migrations.AddField(
            model_name='pantryitem',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
