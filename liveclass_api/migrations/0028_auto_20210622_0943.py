# Generated by Django 3.2.4 on 2021-06-22 09:43

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liveclass_api', '0027_auto_20210622_0940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registeredclass',
            old_name='class_id',
            new_name='class_details',
        ),
        migrations.RenameField(
            model_name='savedclass',
            old_name='class_id',
            new_name='class_details',
        ),
        migrations.AlterField(
            model_name='liveclass_details',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 9, 43, 18, 203211, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='registeredclass',
            unique_together={('class_details', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='savedclass',
            unique_together={('class_details', 'user')},
        ),
    ]