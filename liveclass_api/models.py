from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
    # Create your models here.
    
class LiveClass(models.Model):

    standard = models.IntegerField()
    no_of_students_registered = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Class'
    
    def __str__(self):
        return str(self.standard) + ' class'
    
class User_details(models.Model):
    name = models.OneToOneField(User, on_delete = models.CASCADE, max_length=30)
    standard = models.IntegerField(default=0)
    email = models.EmailField()
    mobile_number = models.IntegerField()
    class Meta:
        verbose_name_plural = 'User_details'

     
    def __str__(self):
        return str(self.name)
    
class Mentor(models.Model):
    name = models.CharField(max_length=30)
    details = models.TextField()
    ratings = models.FloatField(default=0)
    class Meta:
        verbose_name_plural = 'Mentors'
    
    def __str__(self):
        return self.name
    
class LiveClass_details(models.Model):
    standard = models.ForeignKey(LiveClass, on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=30)
    chapter_details = models.TextField()
    mentor_name = models.ForeignKey(Mentor, max_length=30, on_delete=models.CASCADE)
    class_time = models.DateTimeField()
    end_time = models.DateTimeField(default=timezone.now())
    isDoubtClass = models.BooleanField(default=False)
    doubtsAddressed = models.IntegerField(default=0)
    no_of_students_registered = models.IntegerField(default=0)
    no_of_students_attended = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'LiveClass_details'
        
    def __str__(self):
        return self.chapter_name
    
    
    
class SavedClass(models.Model):
    class_details = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta: 
        verbose_name_plural = 'SavedClasses'
    
    def __str__(self):
        return 'SavedClass : ' + str(self.class_details)
    
class RegisteredClass(models.Model):
    class_details = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    class Meta:
        verbose_name_plural = 'RegisteredClass'
        unique_together = ['class_details', 'user']
    
    def __str__(self):
        return 'Registered Class' + str(self.class_details)
    






