# Generated by Django 2.1.4 on 2020-04-21 19:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0006_auto_20200413_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='create_at',
            field=models.DateField(default=datetime.datetime(2020, 4, 21, 19, 46, 42, 745433, tzinfo=utc)),
        ),
    ]
