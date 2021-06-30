# Generated by Django 3.2.4 on 2021-06-28 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liveclass_api', '0067_doubtclasses_registered_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='user',
            field=models.OneToOneField(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_details',
            name='user',
            field=models.OneToOneField(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
