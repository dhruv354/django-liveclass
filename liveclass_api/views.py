from django.shortcuts import redirect
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.serializers import Serializer


from . import serializers
from . import models
# Create your views here.


class IsSuperuserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )


# This view enables the user to see and create a liveclass but creation can only be done by the superuser
class LiveClassView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = models.LiveClass_details.objects.filter(isDraft = False)
    serializer_class = serializers.LiveClass_details_serializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

## this view enables the superuser tom update or delete  a liveclass

class LiveClassViewId(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = models.LiveClass_details.objects.filter(isDraft=False)
    serializer_class = serializers.LiveClass_details_serializer
    permission_classes = [IsAuthenticated]
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


# this view will list all the mentors available
class ListMentors(mixins.ListModelMixin,  generics.GenericAPIView):
    queryset = models.Mentor.objects.all()
    serializer_class = serializers.Mentor_serializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# this view will list all the users available
class ListUserDetails(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.User_details.objects.all()
    serializer_class = serializers.User_details_serializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



#View to see and add a new class to the saved classes
class SavedClassView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    serializer_class = serializers.SavedClass_serializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

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
    

#To delete a particular saved class
class SavedClassDeleteView(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView) :

    serializer_class = serializers.SavedClass_serializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
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
   
    
# to register and deregister a paricular live class 

@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def RegisterClassId(request, id):
    if request.method == 'GET':
        try:
            registered_class = models.RegisteredClass.objects.create(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
            registered_class.save()
            registered_live_class = models.LiveClass_details.objects.get(id=id)
            registered_live_class.no_of_students_registered += 1
            registered_live_class.save()
        except Exception as e:
            return Response("Already registered")
       
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':

        registered_class = models.RegisteredClass.objects.get(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
        registered_class.delete()
        registered_live_class = models.LiveClass_details.objects.get(id=id)
        registered_live_class.no_of_students_registered -= 1
        registered_live_class.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# to get all the registered classes for a particular user

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def RegisterClass(request):
    registered_classes = models.RegisteredClass.objects.filter(user=request.user)
    serializer = serializers.Registered_serializer(registered_classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# to list all the drafts of the classes
class ListDrafts(LoginRequiredMixin, mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = serializers.LiveClass_details_serializer
    queryset = models.LiveClass_details.objects.filter(isDraft=True)

    def get(self, request):
        if request.user.is_superuser:
             return self.list(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        

# to update , view and delete a particular draft
class DraftClassId(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,  mixins.UpdateModelMixin, generics.GenericAPIView):

    serializer_class = serializers.LiveClass_details_serializer
    queryset = models.LiveClass_details.objects.filter(isDraft=True)
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        if request.user.is_superuser:
            if id:
                return self.retrieve(request, id)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    
    def put(self, request, id=None):
        if request.user.is_superuser:
            if id:
                return self.update(request, id)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        

    def delete(self, request, id=None):
        if request.user.is_superuser:
            if id:
                return self.destroy(request, id)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



#view that will list and create all doubtclasses

class DoubtClass( mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = serializers.DoubtClass_serializer
    queryset = models.DoubtClasses.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return self.list(request)

    def post(self, request):
        if request.user.is_superuser:
            return self.create(request)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


#view for a particular doubt class object
class DoubtClassId(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = serializers.DoubtClass_serializer
    queryset = models.DoubtClasses.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None, format=None):
        if id:
            return self.retrieve(request, id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id=None, format=None):
        if id:
            if request.user.is_superuser:
                return self.update(request, id)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, id=None, format=None):
        if id:
            if request.user.is_superuser:
                return self.destroy(request, id)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)



    

#view to list all the chapternames 
class ChapterNames(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.chapterNames_serializer
    # queryset = models.LiveClass_details.objects.filter(id=id).first().chapter_ids.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        #  print(liveclass_id)
        
        liveclass_id = models.LiveClass_details.objects.filter(id=self.kwargs['id']).first()
        print(liveclass_id)
        chapter_names = liveclass_id.chapter_ids.all()
        return chapter_names

    def get(self, request, id=None):
        if id:
            return self.list(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
@api_view(['GET'])

def RegisterClass2(request):
   
    registered_classes = models.RegisteredClassNew.objects.filter(user=request.user)
    serializer = serializers.Registered_serializer(registered_classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to register and deregister a paricular live class 

@api_view(['GET', 'DELETE'])
@login_required
def RegisterClassId2(request, type_of_class, id):
    if type_of_class == 'liveclass':
        if request.method == 'GET':
            try:
                
                registered_class = models.RegisteredClassNew.objects.create(conceptual_class_id=models.LiveClass_details.objects.get(id=id), user=request.user)
                registered_class.save()
                registered_live_class = models.LiveClass_details.objects.get(id=id)
                registered_live_class.no_of_students_registered += 1
                registered_live_class.save()
            except Exception as e:
                return Response("Already registered")
        
            return Response(status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':

            registered_class = models.RegisteredClassNew.objects.get(conceptual_class_id=models.LiveClass_details.objects.get(id=id), user=request.user)
            registered_class.delete()
            registered_live_class = models.LiveClass_details.objects.get(id=id)
            registered_live_class.no_of_students_registered -= 1
            registered_live_class.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif type_of_class == 'doubtclass':
        if request.method == 'GET':
            try:
                registered_class = models.RegisteredClassNew.objects.create(doubtclass_id=models.DoubtClasses.objects.get(id=id), user=request.user)
                registered_class.save()
                registered_doubt_class = models.DoubtClasses.objects.get(id=id)
                registered_doubt_class.no_of_students_registered += 1
                registered_doubt_class.save()
            except Exception as e:
                return Response("Already registered")
        
            return Response(status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':

            registered_class = models.RegisteredClassNew.objects.get(doubtclass_id=models.DoubtClasses.objects.get(id=id), user=request.user)
            registered_class.delete()
            registered_doubt_class  = models.DoubtClasses.objects.get(id=id)
            registered_doubt_class.no_of_students_registered -= 1
            registered_doubt_class.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    