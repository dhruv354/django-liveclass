# Generated by Django 3.2.4 on 2021-06-29 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveclass_api', '0073_alter_liveclass_details_registered_students'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
