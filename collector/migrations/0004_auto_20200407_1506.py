# Generated by Django 2.1.4 on 2020-04-07 20:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_auto_20200407_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='create_at',
            field=models.DateField(default=datetime.datetime(2020, 4, 7, 20, 6, 24, 335674, tzinfo=utc)),
        ),
    ]
