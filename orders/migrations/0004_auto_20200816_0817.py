# Generated by Django 3.0.8 on 2020-08-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200816_0648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='dt_received',
            new_name='date_received',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='dt_thanked',
        ),
        migrations.AddField(
            model_name='donation',
            name='date_thanked',
            field=models.DateField(blank=True, help_text='Who sent the thank-you and how?', null=True, verbose_name='Datetime thanked'),
        ),
        migrations.AddField(
            model_name='donation',
            name='payment_details',
            field=models.CharField(blank=True, help_text='Check #, Credit Card type, etc.', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='notes',
            field=models.TextField(blank=True, help_text='Any additional notes on this donation?', null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='thanked_by',
            field=models.CharField(blank=True, help_text='Who sent the thank-you and how?', max_length=254, null=True),
        ),
    ]
