# Generated by Django 3.1.13 on 2021-07-08 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterNames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_names', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoubtClasses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doubtClass_details', models.TextField()),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('doubtsAddressed', models.IntegerField(default=0)),
                ('ratings', models.FloatField(default=0)),
                ('no_of_students_registered', models.IntegerField(default=0)),
                ('no_of_students_attended', models.IntegerField(default=0)),
                ('isDraft', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'DoubtClasses',
            },
        ),
        migrations.CreateModel(
            name='LiveClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard', models.IntegerField()),
                ('no_of_students_registered', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Class',
            },
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('details', models.TextField()),
                ('ratings', models.FloatField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Mentors',
            },
        ),
        migrations.CreateModel(
            name='RegisteredNames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.IntegerField(default=0)),
                ('email', models.EmailField(default='abc@gmail.com', max_length=254)),
                ('mobile_number', models.IntegerField(default=0)),
                ('name', models.OneToOneField(max_length=30, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User_details',
            },
        ),
        migrations.CreateModel(
            name='LiveClass_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_details', models.TextField(default='')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('doubtsAddressed', models.IntegerField(default=0)),
                ('isDraft', models.BooleanField(default=True)),
                ('ratings', models.FloatField(default=0)),
                ('group', models.IntegerField(default=0)),
                ('quizzes', models.IntegerField(default=0)),
                ('no_of_students_registered', models.IntegerField(default=0)),
                ('no_of_students_attended', models.IntegerField(default=0)),
                ('chapter_ids', models.ManyToManyField(to='liveclass_api.ChapterNames')),
                ('doubtClass', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.doubtclasses')),
                ('mentor_id', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.mentor')),
                ('registered_students', models.ManyToManyField(blank=True, null=True, to='liveclass_api.RegisteredNames')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.liveclass')),
            ],
            options={
                'verbose_name_plural': 'LiveClass_details',
            },
        ),
        migrations.AddField(
            model_name='doubtclasses',
            name='mentor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.mentor'),
        ),
        migrations.AddField(
            model_name='doubtclasses',
            name='registered_students',
            field=models.ManyToManyField(blank=True, null=True, to='liveclass_api.RegisteredNames'),
        ),
        migrations.CreateModel(
            name='SavedClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.liveclass_details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'SavedClasses',
                'unique_together': {('class_details', 'user')},
            },
        ),
        migrations.CreateModel(
            name='RegisteredClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.FloatField(default=0)),
                ('class_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.liveclass_details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'RegisteredClass',
                'unique_together': {('class_details', 'user')},
            },
        ),
        migrations.CreateModel(
            name='RegisterDoubtClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.FloatField(default=0)),
                ('doubtclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liveclass_api.doubtclasses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'RegisteDoubtClass',
                'unique_together': {('doubtclass', 'user')},
            },
        ),
    ]
