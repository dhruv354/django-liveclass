from rest_framework import serializers
from . import models



class LiveClass_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.LiveClass
        fields = '__all__'


class SavedClass_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.SavedClass
        fields = '__all__'

class User_details_serializer(serializers.ModelSerializer):
    saved_class = SavedClass_serializer()
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

class Registered_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegisteredClass
        fields = '__all__'








