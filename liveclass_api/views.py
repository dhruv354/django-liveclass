from django.shortcuts import redirect
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse



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



#api endpoints to save  and register live classes 

class SavedClassView(LoginRequiredMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    serializer_class = serializers.SavedClass_serializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return models.SavedClass.objects.filter(user=self.request.user.id)

    def get_object(self):
        return super().get_object()
    
    def get(self, request):
        print(dir(self.request.data.values()))
        return self.list(request)


    def post(self, request):
        cur_user = self.request.user
        if int(request.POST.get('user')) != self.request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
        return self.create(request)
    

class SavedClassDeleteView(LoginRequiredMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView) :

    serializer_class = serializers.SavedClass_serializer
    lookup_field = 'id'
    # queryset = models.SavedClass.objects.filter(user=self.request.user.id)
    def get_queryset(self):
        user = self.request.user
        return models.SavedClass.objects.filter(user=self.request.user.id)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        return Response("no content", status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, id=None):
        try:
             self.destroy(request, id)
             return redirect('saved')
        except Exception as e:
            return Response(Exception, status=status.HTTP_400_BAD_REQUEST)
   
    
@login_required
@api_view(['GET', 'DELETE'])
def RegisterClassId(request, id):
    if request.method == 'GET':
        try:
            registered_class = models.RegisteredClass.objects.create(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
            registered_class.save()
            registered_live_class = models.LiveClass_details.objects.get(id=id)
            registered_live_class.no_of_students_registered += 1
            registered_live_class.save()
        except Exception as e:
            print(e)
       
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':

        registered_class = models.RegisteredClass.objects.get(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
        registered_class.delete()
        registered_live_class = models.LiveClass_details.objects.get(id=id)
        registered_live_class.no_of_students_registered -= 1
        registered_live_class.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
@login_required
@api_view(['GET'])
def RegisterClass(request):
    registered_classes = models.RegisteredClass.objects.filter(user=request.user)
    serializer = serializers.Registered_serializer(registered_classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class DoubtClass(LoginRequiredMixin, mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = serializers.LiveClass_details_serializer

    def get_queryset(self):
        return models.LiveClass_details.objects.filter(isDoubtClass = True)
    
    def get(self, request):
        return self.list(request)

    

    


