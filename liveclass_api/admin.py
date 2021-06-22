from django.contrib import admin
from .models import LiveClass, User_details, Mentor, LiveClass_details, SavedClass, RegisteredClass, ChapterNames
# Register your models here.
admin.site.register([LiveClass, User_details, Mentor, LiveClass_details,SavedClass, RegisteredClass, ChapterNames])