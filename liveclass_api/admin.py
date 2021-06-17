from django.contrib import admin
from .models import LiveClass, User_details, Mentor, LiveClass_details, LiveClass_registration
# Register your models here.
admin.site.register([LiveClass, User_details, Mentor, LiveClass_details, LiveClass_registration])