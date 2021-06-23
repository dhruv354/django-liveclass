from django.core.exceptions import ValidationError
from liveclass_api.models import LiveClass
from django.db import models
from liveclass_api.models import LiveClass_details, LiveClass, Mentor, DoubtClasses
from django.contrib.auth.models import User
# Create your models here.



class AnswersModel(models.Model):
    answer = models.TextField()



class QuestionModel(models.Model):
    question = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    doubt_class_id = models.ForeignKey(DoubtClasses, on_delete=models.CASCADE)
    conceptual_class_id = models.ForeignKey(LiveClass_details, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    def clean(self):
        if self.doubt_class_id and self.conceptual_class_id :
            raise ValidationError("only one field can be set")

class AnswersModel(models.Model):
    answer = models.TextField()
    question_id = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)


