from django.contrib import admin

# Register your models here.
from .models import QuestionModel, Mentors
admin.site.register([QuestionModel, Mentors])