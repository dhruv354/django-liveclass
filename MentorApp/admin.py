from django.contrib import admin

# Register your models here.
from .models import QuestionModel, AnswersModel


class QuestionAdmin(admin.ModelAdmin):

    readonly_fields = ['answer']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return self.readonly_fields

admin.site.register(QuestionModel, QuestionAdmin)
