# Generated by Django 3.0.8 on 2020-08-16 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200816_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='date_received',
            field=models.DateField(blank=True, null=True, verbose_name='Date donation received'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='date_thanked',
            field=models.DateField(blank=True, help_text='Who sent the thank-you and how?', null=True, verbose_name='Date thanked'),
        ),
    ]
