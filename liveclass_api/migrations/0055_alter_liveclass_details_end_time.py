# Generated by Django 3.2.4 on 2021-06-23 17:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0054_alter_liveclass_details_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liveclass_details',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 23, 17, 56, 25, 206610, tzinfo=utc)),
        ),
    ]
