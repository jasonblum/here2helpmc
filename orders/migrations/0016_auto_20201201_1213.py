# Generated by Django 3.0.8 on 2020-12-01 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20201130_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supporter',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
