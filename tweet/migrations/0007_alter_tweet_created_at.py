# Generated by Django 4.0.6 on 2022-07-14 09:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0006_alter_tweet_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 14, 9, 20, 50, 207590, tzinfo=utc)),
        ),
    ]