# Generated by Django 3.0.4 on 2020-04-11 10:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ration', '0004_auto_20200411_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rationallocation',
            name='allocation_expiry',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 12, 10, 58, 43, 60497, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rationallocation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
