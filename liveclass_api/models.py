from django.db import models

# Create your models here.

class LiveClass(models.Model):
    standard = models.IntegerField()
    no_of_students_registered = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Class'

class User_details(models.Model):
    name = models.CharField(max_length=30)
    standard = models.ForeignKey(LiveClass, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30)
    mobile_number = models.IntegerField()
    class Meta:
        verbose_name_plural = 'User_details'


class Mentor(models.Model):
    name = models.CharField(max_length=30)
    details = models.TextField()
    class Meta:
        verbose_name_plural = 'Mentors'


class LiveClass_details(models.Model):
    standard = models.ForeignKey(LiveClass, on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=30)
    chapter_details = models.TextField()
    mentor_name = models.ForeignKey(Mentor, max_length=30, on_delete=models.CASCADE)
    class_time = models.DateTimeField()
    class Meta:
        verbose_name_plural = 'LiveClass_details'

class LiveClass_registration(models.Model):
    class_details = models.OneToOneField(LiveClass_details, on_delete=models.CASCADE)
    name = models.OneToOneField(User_details, on_delete=models.CASCADE)

    class Meta: 
         verbose_name_plural = 'LiveClass_registration'






