# Generated by Django 3.2.4 on 2021-06-22 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mentors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionmodel',
            name='doubt_class',
        ),
        migrations.RemoveField(
            model_name='questionmodel',
            name='mentor',
        ),
        migrations.DeleteModel(
            name='Mentors',
        ),
        migrations.DeleteModel(
            name='QuestionModel',
        ),
    ]
