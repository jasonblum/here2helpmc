# Generated by Django 3.0.8 on 2020-12-07 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0027_deliveryday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveryday',
            old_name='date',
            new_name='_date',
        ),
    ]
