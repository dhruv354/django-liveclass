# Generated by Django 3.2.4 on 2021-06-23 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mentors', '0005_alter_questionmodel_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionmodel',
            name='answer',
            field=models.TextField(blank=True, null=True),
        ),
    ]
