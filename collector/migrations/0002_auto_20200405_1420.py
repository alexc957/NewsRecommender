# Generated by Django 2.1.4 on 2020-04-05 19:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='create_at',
            field=models.DateField(default=datetime.datetime(2020, 4, 5, 19, 20, 8, 785388, tzinfo=utc)),
        ),
    ]
