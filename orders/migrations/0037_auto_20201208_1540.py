# Generated by Django 3.0.8 on 2020-12-08 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0036_auto_20201208_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryday',
            name='_week_of_year',
            field=models.PositiveSmallIntegerField(blank=True),
        ),
    ]