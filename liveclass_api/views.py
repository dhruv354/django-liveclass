from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response


from . import serializers
from . import models
# Create your views here.

class ListLiveClass(mixins.ListModelMixin, LoginRequiredMixin, generics.GenericAPIView):
    queryset = models.LiveClass_details.objects.all()
    serializer_class = serializers.LiveClass_details_serializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class LiveClassView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    LoginRequiredMixin,
                    generics.GenericAPIView):
    queryset = models.LiveClass_details.objects.all()
    serializer_class = serializers.LiveClass_details_serializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class LiveClassViewId(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    LoginRequiredMixin,
                    generics.GenericAPIView):
    queryset = models.LiveClass_details.objects.all()
    serializer_class = serializers.LiveClass_details_serializer
    lookup_field = 'id'

    def get(self, request, id=None, format=None):
        if id:
           return self.retrieve(request)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):

        if request.user.is_superuser:
            return self.update(request, id)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id, format=None):
        if request.user.is_superuser:
            return self.destroy(request, id)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ListMentors(mixins.ListModelMixin, LoginRequiredMixin, generics.GenericAPIView):
    queryset = models.Mentor.objects.all()
    serializer_class = serializers.Mentor_serializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class ListUserDetails(mixins.ListModelMixin, LoginRequiredMixin, generics.GenericAPIView):
    queryset = models.User_details.objects.all()
    serializer_class = serializers.User_details_serializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

