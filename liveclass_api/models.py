from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError



    # Create your models here.


# class CustomUser(AbstractUser):

#     CHOICES = (
#         ('M', 'Mentor'),
#         ('S', 'Student'),
#     )
#     role = models.CharField(max_length=1, choices=CHOICES)
    

# model to store Class standard and can be added certain things that are specific to the standard
class LiveClass(models.Model):

    standard = models.IntegerField()
    no_of_students_registered = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Class'
    
    def __str__(self):
        return str(self.standard) + ' class'
    
# contains current user details
class User_details(models.Model):
    name = models.OneToOneField(User, on_delete = models.CASCADE, max_length=30)
    username = models.CharField(max_length=50, null=True, blank=True)
    standard = models.IntegerField(default=0)
    email = models.EmailField(default='abc@gmail.com')
    mobile_number = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'User_details'

     
    def __str__(self):
        return str(self.name)
    

#live class mentors details
class Mentor(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(null=True, blank=True)
    details = models.TextField()
    ratings = models.FloatField(default=0)
    class Meta:
        verbose_name_plural = 'Mentors'
    
    def __str__(self):
        return self.name


class ChapterNames(models.Model):
    chapter_names = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.chapter_names


class RegisteredNames(models.Model):
    name = models.CharField(max_length=100, unique=True)




#model for doubt classes
class DoubtClasses(models.Model):
    doubtClass_details = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    doubtsAddressed = models.IntegerField(default=0)
    ratings = models.FloatField(default=0)
    registered_students = models.ManyToManyField(RegisteredNames, null=True, blank=True)
    no_of_students_registered = models.IntegerField(default=0)
    no_of_students_attended = models.IntegerField(default=0)
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'DoubtClasses'
    
    def __str__(self):
        return self.doubtClass_details

    
# conceptual class details model containing all relevant information possible for the class
class LiveClass_details(models.Model):
    standard = models.ForeignKey(LiveClass, on_delete=models.CASCADE)
    chapter_ids = models.ManyToManyField(ChapterNames)
    chapter_details = models.TextField(default='')
    mentor_id = models.ForeignKey(Mentor, max_length=30, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    doubtClass = models.OneToOneField(DoubtClasses, on_delete=models.PROTECT, null=True, blank=True)
    doubtsAddressed = models.IntegerField(default=0)
    isDraft = models.BooleanField(default=True)
    ratings = models.FloatField(default=0)
    no_of_students_registered = models.IntegerField(default=0)
    registered_students = models.ManyToManyField(RegisteredNames, null=True, blank=True)
    no_of_students_attended = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'LiveClass_details'
        
    def __str__(self):
        return self.chapter_details
    
    
#list of saved classes by the students

class SavedClass(models.Model):
    class_details = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta: 
        verbose_name_plural = 'SavedClasses'
        unique_together = ['class_details', 'user']
    
    def __str__(self):
        return 'SavedClass : ' + str(self.class_details)
    
#list of registered classes by the students
class RegisteredClass(models.Model):
    class_details = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.FloatField(default=0)
        
    class Meta:
        verbose_name_plural = 'RegisteredClass'
        unique_together = ['class_details', 'user']
    
    def __str__(self):
        return 'Registered Class' + str(self.class_details)
    

class RegisterDoubtClass(models.Model):
    doubtclass = models.ForeignKey(DoubtClasses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.FloatField(default=0)
        
    class Meta:
        verbose_name_plural = 'RegisteDoubtClass'
        unique_together = ['doubtclass', 'user']


   

#         # try:
#         #     RegisteredClassNew.objects.get(user=self.cleaned_data['user'], 
#         #                         doubtclass_id=self.cleaned_data['doubtclass_id'],
#         #                         conceptual_class_id=self.cleaned_data['conceptual_class_id']
#         #                        )
#         #     #if we get this far, we have an exact match for this form's data
#         #     raise ValidationError("Exists already!")
#         # except RegisteredClassNew.DoesNotExist:
#         #     #because we didn't get a match
#         #     pass

#         # return self.cleaned_data




        





