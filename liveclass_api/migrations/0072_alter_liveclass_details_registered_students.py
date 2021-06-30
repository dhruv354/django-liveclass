# Generated by Django 3.2.4 on 2021-06-29 15:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liveclass_api', '0071_alter_liveclass_details_registered_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liveclass_details',
            name='registered_students',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
