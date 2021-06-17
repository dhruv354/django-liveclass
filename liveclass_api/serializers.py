from rest_framework import serializers
from . import models



class LiveClass_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.LiveClass
        fields = '__all__'


class User_details_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.User_details
        fields = '__all__'


class LiveClass_details_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.LiveClass_details
        fields = '__all__'

class Mentor_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mentor
        fields = '__all__'

class LiveClass_registration_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.LiveClass_registration
        fields = '__all__'






