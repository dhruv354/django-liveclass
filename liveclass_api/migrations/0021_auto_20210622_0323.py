# Generated by Django 3.2.4 on 2021-06-22 03:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0020_alter_liveclass_details_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapternames',
            name='chapter_names',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='liveclass_details',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 3, 23, 37, 834882, tzinfo=utc)),
        ),
    ]
