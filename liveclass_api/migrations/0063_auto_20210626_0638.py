# Generated by Django 3.2.4 on 2021-06-26 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0062_auto_20210626_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerdoubtclass',
            name='ratings',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='registeredclass',
            name='ratings',
            field=models.FloatField(default=0),
        ),
    ]