# Generated by Django 3.0.8 on 2020-12-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_delete_deliveryday'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_updated', models.DateTimeField(auto_now=True, verbose_name='Datetime updated')),
                ('date', models.DateField(unique=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
