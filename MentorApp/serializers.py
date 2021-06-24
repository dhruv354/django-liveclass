from rest_framework import fields, serializers
from . import models



class QuestionModel_serializer(serializers.ModelSerializer):

    class Meta():
        model = models.QuestionModel
        fields = '__all__'


class AnswerModel_serializer(serializers.ModelSerializer):

    class Meta():
        model = models.AnswersModel
        fields = '__all__'

