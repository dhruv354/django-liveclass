# Generated by Django 3.2.4 on 2021-06-29 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0069_auto_20210628_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='email',
            field=models.EmailField(default='abc@gmail.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='mobile_number',
            field=models.IntegerField(default=0),
        ),
    ]
