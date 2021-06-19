# Generated by Django 3.2.4 on 2021-06-19 13:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liveclass_api', '0010_auto_20210619_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liveclass_details',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 19, 13, 30, 32, 831012, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='RegisteredClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.liveclass_details')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'SavedClasses',
            },
        ),
    ]
