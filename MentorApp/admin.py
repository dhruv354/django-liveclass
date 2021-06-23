from django.contrib import admin

# Register your models here.
from .models import QuestionModel, AnswersModel

admin.site.register([QuestionModel, AnswersModel])