# Generated by Django 3.2.4 on 2021-06-26 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0063_auto_20210626_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doubtclasses',
            name='ratings',
            field=models.FloatField(default=0),
        ),
    ]
