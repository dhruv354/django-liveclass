from django.contrib import admin

# Register your models here.
from .models import QuestionModel, AnswersModel


class QuestionAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append('answer')
        return fields
admin.site.register(QuestionModel, QuestionAdmin)
