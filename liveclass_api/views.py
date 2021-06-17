from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics


from . import serializers
from . import models
# Create your views here.

class ListLiveClass(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.LiveClass_details.objects.all()
    serializer_class = serializers.LiveClass_details_serializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ListMentors(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Mentor.objects.all()
    serializer_class = serializers.Mentor_serializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
