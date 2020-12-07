# Generated by Django 3.0.8 on 2020-12-07 15:44

import address.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_auto_20160213_1726'),
        ('orders', '0029_auto_20201207_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_updated', models.DateTimeField(auto_now=True, verbose_name='Datetime updated')),
                ('status', models.CharField(choices=[('created', 'Created'), ('processed', 'Processed and Assigned a Driver'), ('ready', 'Ready for Delivery'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='created', max_length=9)),
                ('customer_zip', models.CharField(max_length=5)),
                ('dt_ready', models.DateTimeField(blank=True, null=True, verbose_name='Datetime ready')),
                ('dt_delivered', models.DateTimeField(blank=True, null=True, verbose_name='Datetime delivered')),
                ('dt_cancelled', models.DateTimeField(blank=True, null=True, verbose_name='Datetime cancelled')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.Customer')),
                ('deliver_to_address', address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.Address', verbose_name='Street Address Delivered')),
                ('deliveryday', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.DeliveryDay')),
                ('driver', models.ForeignKey(blank=True, limit_choices_to={'is_driver': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.Supporter')),
            ],
            options={
                'ordering': ['-dt_created'],
            },
        ),
    ]
