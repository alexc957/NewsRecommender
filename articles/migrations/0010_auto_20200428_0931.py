# Generated by Django 2.1.4 on 2020-04-28 14:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_article_date_uploaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2020, 4, 28, 14, 31, 29, 52106, tzinfo=utc)),
        ),
    ]
