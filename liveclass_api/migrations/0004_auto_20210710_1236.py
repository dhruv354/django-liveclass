# Generated by Django 3.1.13 on 2021-07-10 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0003_auto_20210709_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerdoubtclass',
            name='ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='registeredclass',
            name='ratings',
            field=models.IntegerField(default=0),
        ),
    ]