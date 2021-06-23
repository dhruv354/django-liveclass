from liveclass_api.models import LiveClass
from django.db import models
from liveclass_api.models import LiveClass_details, LiveClass
from django.contrib.auth.models import User
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
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    doubt_class = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentors, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.question


