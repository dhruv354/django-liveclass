from liveclass_api.models import LiveClass
from django.db import models
from liveclass_api.models import LiveClass_details, LiveClass
# Create your models here.

class Mentors(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    ratings = models.IntegerField(default=0)
    details = models.TextField()


    class Meta:
        verbose_name_plural = 'Mentors'
    
    def __str__(self):
        return self.name

class QuestionModel(models.Model):
    question = models.TextField()
    doubt_class = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentors, on_delete=models.CASCADE)
    answer = models.TextField()
    status = models.BooleanField(default=False)


