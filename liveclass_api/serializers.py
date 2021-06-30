from rest_framework import fields, serializers
from rest_framework.views import set_rollback
from . import models



#serializers for all the models containing which items to show 

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

class chapterNames_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChapterNames
        fields = '__all__'


class LiveClass_details_serializer(serializers.ModelSerializer):
    chapter_names = chapterNames_serializer(read_only=True, many=True)
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


class DoubtClass_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoubtClasses
        fields = '__all__'

class RegisterDoubtclass_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegisterDoubtClass
        fields = '__all__'


class RegisterNames_serializer(serializers.ModelSerializer):
      class Meta:
        model = models.RegisteredNames
        fields = '__all__'





