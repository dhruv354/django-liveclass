# Generated by Django 3.2.4 on 2021-06-30 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MentorApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionmodel',
            name='status',
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='answer',
            field=models.TextField(default=''),
        ),
    ]
