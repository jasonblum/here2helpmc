# Generated by Django 3.0.8 on 2020-08-16 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='dt_received',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Datetime donation received'),
        ),
        migrations.AddField(
            model_name='donation',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='thanked_by',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='method',
            field=models.CharField(choices=[('cash', 'Cash'), ('check', 'Check'), ('credit', 'Credit'), ('paypal', 'PayPal'), ('venmo', 'Venmo')], max_length=6),
        ),
    ]
