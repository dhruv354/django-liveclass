from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from liveclass_api.models import LiveClass
from django.db import models
from liveclass_api.models import LiveClass_details, LiveClass, Mentor, DoubtClasses
from django.contrib.auth.models import User
# Create your models here.





class QuestionModel(models.Model):
    question = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    doubt_class_id = models.ForeignKey(DoubtClasses, on_delete=models.CASCADE, null=True, blank=True)
    conceptual_class_id = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE, null=True, blank=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.TextField(default="", blank=True)

    def __str__(self):
        return self.question

    def clean(self):
        if self.doubt_class_id != None and self.conceptual_class_id !=None :
            raise ValidationError("only one type of class can be selected ")
        
        elif  not self.doubt_class_id and not self.conceptual_class_id:
            raise ValidationError("both type of class cannot be empty")

        
    

class AnswersModel(models.Model):
    answer = models.TextField()
    question_id = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)


    class Meta:
        pass




