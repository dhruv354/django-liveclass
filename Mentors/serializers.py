from rest_framework import fields, serializers
from . import models



class QuestionModel_serializer(serializers.ModelSerializer):

    class Meta():
        model = models.QuestionModel
        fields = '__all__'


class Mentor_serializer(serializers.ModelSerializer):

    class Meta():
        model = models.Mentors
        fields = '__all__'