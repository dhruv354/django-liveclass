# Generated by Django 3.2.4 on 2021-06-26 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0061_auto_20210625_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerdoubtclass',
            name='ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='registeredclass',
            name='ratings',
            field=models.IntegerField(default=0),
        ),
    ]
