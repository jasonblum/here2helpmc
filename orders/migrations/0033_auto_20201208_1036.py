# Generated by Django 3.0.8 on 2020-12-08 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_auto_20201208_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='requires_admin_attention',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime created'),
        ),
        migrations.AlterField(
            model_name='deliveryday',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime created'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime created'),
        ),
        migrations.AlterField(
            model_name='dropofflocation',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime created'),
        ),
        migrations.AlterField(
            model_name='order',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime created'),
        ),
        migrations.AlterField(
            model_name='school',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime created'),
        ),
        migrations.AlterField(
            model_name='supporter',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime created'),
        ),
    ]