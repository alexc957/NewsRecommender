# Generated by Django 2.1.4 on 2020-04-28 14:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0014_auto_20200428_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='create_at',
            field=models.DateField(default=datetime.datetime(2020, 4, 28, 14, 31, 29, 52106, tzinfo=utc)),
        ),
    ]
