# Generated by Django 2.1.4 on 2020-04-22 19:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0012_auto_20200422_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='create_at',
            field=models.DateField(default=datetime.datetime(2020, 4, 22, 19, 44, 47, 597353, tzinfo=utc)),
        ),
    ]
