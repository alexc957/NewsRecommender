# Generated by Django 2.1.5 on 2020-04-29 20:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20200429_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2020, 4, 29, 20, 51, 50, 496422, tzinfo=utc)),
        ),
    ]
