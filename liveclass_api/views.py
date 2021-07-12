from typing import Generic
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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
import datetime 
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.serializers import Serializer
from django_zoom_meetings import ZoomMeetings
from .zoom_credentials import credentials
import json
import jwt
import http
import requests


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


# to get metors by id
class MentorsId(mixins.RetrieveModelMixin, generics.GenericAPIView):
    lookup_field = 'id'
    serializer_class = serializers.Mentor_serializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return models.Mentor.objects.filter(id=self.kwargs['id'])

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
            # print(type(request.data))
            token = jwt.encode(
        
        # Create a payload of the token containing 
        # API Key & expiration time
                {'iss': credentials['API-KEY'], 'exp': time.time() + 5000},
                
                # Secret used to generate token signature
                credentials['API-SECRET'],
                
                # Specify the hashing alg
                algorithm='HS256'
            )
            # payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            #        'iss': credentials['API-KEY']
            #       }     
            # token = jwt.encode(payload, credentials['API-SECRET']).decode("utf-8")
            print(request.data)

            token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IldqOGFLU0lTUm5lNDhucnFCS3BPQlEiLCJleHAiOjE2MjY2NjI1NzQsImlhdCI6MTYyNjA1Nzc3NX0.rb55SRVcByMkr1Iy0D_lc7g041bWlbeCUFoMD8rGBgk'
            headers = {'authorization': 'Bearer %s' % token,
                    'content-type': 'application/json'}
            print(type(request.data))
            print(request.data['start_time'])
            print(request.data['chapter_details'])
            
            meetingdetails = {"topic": str(request.data['chapter_details']),
                  "type": 2,
                  "start_time": str(request.data['start_time']),
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",
  
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }
  

            r = requests.post(
                f'https://api.zoom.us/v2/users/me/meetings', 
            headers=headers, data=json.dumps(meetingdetails))
        
            print("\n creating zoom meeting ... \n")

            print(r.json())
            y = json.loads(r.text)
            join_URL = y["join_url"]
            request.data._mutable = True
            request.data['meeting_url'] = join_URL
            request.data['meeting_id'] = str(r.json()['id'])
            request.data._mutable = False
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


    # def post(self, request):
    #     cur_user = self.request.user
    #     if int(request.POST.get('user')) != self.request.user.id:
    #             return Response(status=status.HTTP_403_FORBIDDEN)
    #     return self.create(request)
    

#To delete a particular saved class

# class SavedClassDeleteView(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView) :

#     serializer_class = serializers.SavedClass_serializer
#     lookup_field = 'id'
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         user = self.request.user
#         return models.SavedClass.objects.filter(user=self.request.user.id)

#     def get(self, request, id=None):
#         if id:
#             return self.retrieve(request, id)
#         return Response("no content", status=status.HTTP_204_NO_CONTENT)
    
#     def delete(self, request, id=None):
#         try:
#              self.destroy(request, id)
#              return redirect('saved')
#         except Exception as e:
#             return Response(Exception, status=status.HTTP_400_BAD_REQUEST)
   


@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def SavedClassId(request, id):
    if request.method == 'GET':
        if not models.LiveClass_details.objects.filter(id=id).exists():
            return Response("id with this liveclass does not exist", status=status.HTTP_400_BAD_REQUEST)
        try:
            saved_class = models.SavedClass.objects.create(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
            saved_class.save()
        except Exception as e:
            return Response("Already Saved")
       
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':

        saved_class = models.SavedClass.objects.get(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
        saved_class.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
# to register and deregister a paricular live class 

@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def RegisterClassId(request, id):
    print(request.method)

    if request.method == 'GET':
        try:
            registered_class = models.RegisteredClass.objects.create(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
            registered_class.save()
            liveclass = models.LiveClass_details.objects.get(id=id)
            #print("liveclass: ", liveclass )
            try:
                registered_student = models.RegisteredNames(name=request.user.username)
                registered_student.save()
            except:
                registered_student = models.RegisteredNames.objects.filter(name=request.user.username).first()
            liveclass.registered_students.add(registered_student)
            # liveclass.save()
            # registered_doubt_class = models.DoubtClasses.objects.get(id=id)
            liveclass.no_of_students_registered += 1
            liveclass.no_of_students_attended += 1
            liveclass.save()
        except Exception as e:
            return Response("Already registered")
       
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        print("in delete method")
        registered_class = models.RegisteredClass.objects.get(class_details=models.LiveClass_details.objects.get(id=id), user=request.user)
        print("registere_class : ", registered_class)
        registered_class.delete()
        # registered_class.save()
        registered_live_class = models.LiveClass_details.objects.get(id=id)
        if(registered_live_class.no_of_students_registered > 0):
            registered_live_class.no_of_students_registered -= 1
            registered_live_class.no_of_students_attended -= 1
        registered_live_class.save()
        print('error here')
        registered_name = models.RegisteredNames.objects.filter(name=request.user.username).first()
        print('error after registered name')
        print(registered_name)
        registered_live_class.registered_students.remove(registered_name.id)
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
class ListDrafts(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = serializers.LiveClass_details_serializer
    queryset = models.LiveClass_details.objects.filter(isDraft=True)
    permission_classes = [IsAuthenticated]

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


class ListDoubtDrafts(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.DoubtClass_serializer
    queryset = models.DoubtClasses.objects.filter(isDraft=True)
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_superuser:
             return self.list(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class DoubtDraftClassId(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,  mixins.UpdateModelMixin, generics.GenericAPIView):

    serializer_class = serializers.DoubtClass_serializer
    queryset = models.DoubtClasses.objects.filter(isDraft=True)
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
    serializer_class = serializers.ChapterNames_serializer
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



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def RegisterDoubtClass(request):
   
    registered_classes = models.RegisterDoubtClass.objects.filter(user=request.user)
    serializer = serializers.RegisterDoubtclass_serializer(registered_classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def RegisterDoubtClassId(request, id):
   
    if request.method == 'GET':
        try:
            registered_class = models.RegisterDoubtClass.objects.create(doubtclass=models.DoubtClasses.objects.get(id=id), user=request.user)
            registered_class.save()
            liveclass = models.DoubtClasses.objects.get(id=id)
            #print("liveclass: ", liveclass )
            try:
                registered_student = models.RegisteredNames(name=request.user.username)
                registered_student.save()
            except:
                registered_student = models.RegisteredNames.objects.filter(name=request.user.username).first()
            liveclass.registered_students.add(registered_student)
            liveclass.save()
            registered_doubt_class = models.DoubtClasses.objects.get(id=id)
            registered_doubt_class.no_of_students_registered += 1
            registered_doubt_class.no_of_students_attended += 1
            registered_doubt_class.save()
        except Exception as e:
            return Response("Already registered")
       
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':

        registered_class = models.RegisterDoubtClass.objects.get(doubtclass=models.DoubtClasses.objects.get(id=id), user=request.user)
        registered_class.delete()
        # liveclass = models.DoubtClasses.objects.get(id=id)
        registered_live_class = models.DoubtClasses.objects.get(id=id)
        if(registered_live_class.no_of_students_registered > 0):
            registered_live_class.no_of_students_registered -= 1
            registered_live_class.no_of_students_attended -= 1
        registered_live_class.save()
        print('error here')
        registered_name = models.RegisteredNames.objects.filter(name=request.user.username).first()
        registered_live_class.registered_students.remove(registered_name.id)
        registered_live_class.save()
    
# @csrf_exempt
# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# def liveclassRatings(request, id):
#     print((request.body))
#     print(request.user.id)

    
#     registered_class = models.RegisteredClass.objects.get(user=request.user.id, id=id)
#     liveclass_id = registered_class.class_details.id
#     print("liveclass id: ",liveclass_id)
#     current_ratings = registered_class.ratings
#     data = json.loads(request.body)
#     new_ratings = data['ratings']
#     print("error here regsiteredclass.ratings")
#     registered_class.ratings = new_ratings

#     registered_class.save()
#     liveclass = models.LiveClass_details.objects.get(id=liveclass_id)
#     total_ratings = liveclass.ratings * liveclass.no_of_students_registered
#     total_ratings = total_ratings - current_ratings + new_ratings
#     students_registered = liveclass.no_of_students_registered
#     liveclass.ratings = total_ratings/students_registered
#     liveclass.save()
#     return Response("your ratings noted", status=status.HTTP_200_OK)



@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def liveclassRatings(request, id):
    # print((request.body))
    print(request.user.id)

    
    registered_class = models.RegisteredClass.objects.get(user=request.user.id, class_details=id)
    liveclass_id = models.LiveClass_details.objects.get(id=id)
    print("liveclass id: ",liveclass_id)
    current_ratings = registered_class.ratings
    total_ratings_initial = liveclass_id.ratings * liveclass_id.no_of_students_rated
   
    #current ratings 0 indicates that the user hasn't rated yet
    if current_ratings == 0:
        liveclass_id.no_of_students_rated += 1
        liveclass_id.save()
    data = request.data
    print("error here ")
    new_ratings = data['ratings']
    print(new_ratings)
    if new_ratings == 0:
        if current_ratings == 0:
            liveclass_id.no_of_students_rated -= 1
            liveclass_id.save()
        return Response("minimum allowed rating is 1 so update your rating", status=status.HTTP_400_BAD_REQUEST)
    registered_class.ratings = new_ratings

    registered_class.save()
    liveclass = models.LiveClass_details.objects.get(id=id)
    students_rated = liveclass.no_of_students_rated
    # total_ratings = liveclass.ratings * students_rated
    total_ratings = total_ratings_initial - current_ratings + new_ratings
    print(total_ratings)
    if total_ratings == 0 or students_rated == 0:
        return Response("students must rate", status=status.HTTP_400_BAD_REQUEST)
    liveclass.ratings = total_ratings/students_rated
    liveclass.save()
    return Response("your ratings noted", status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def DoubtclassRatings(request, id):
    # print((request.body))
    # print(request.user.id)

    
    registered_class = models.RegisterDoubtClass.objects.get(user=request.user.id, doubtclass=id)
    doubtclass_id = models.DoubtClasses.objects.get(id=id)
    print("liveclass id: ",doubtclass_id)
    current_ratings = registered_class.ratings
    total_ratings_initial = doubtclass_id.ratings * doubtclass_id.no_of_students_rated
    #current ratings 0 indicates that the user hasn't rated yet
    if current_ratings == 0:
        doubtclass_id.no_of_students_rated += 1
        doubtclass_id.save()
    data = request.data
    new_ratings = data['ratings']
    if new_ratings == 0:
        if current_ratings == 0:
            doubtclass_id.no_of_students_rated -= 1
            doubtclass_id.save()
        return Response("minimum allowed rating is 1 so update your rating", status=status.HTTP_400_BAD_REQUEST)
    registered_class.ratings = new_ratings

    registered_class.save()
    doubtclass = models.DoubtClasses.objects.get(id=id)
    students_rated = doubtclass.no_of_students_rated
    # total_ratings = doubtclass.ratings * students_rated
    total_ratings = total_ratings_initial - current_ratings + new_ratings
    if total_ratings == 0 or students_rated == 0:
        return Response("students must rate", status=status.HTTP_400_BAD_REQUEST)
    doubtclass.ratings = total_ratings/students_rated
    doubtclass.save()
    return Response("your ratings noted", status=status.HTTP_200_OK)
    # except Exception as e:
    #     print(e)
    #     return Response(e, status=status.HTTP_400_BAD_REQUEST)




# # to register and deregister a paricular live class 

# @api_view(['GET', 'DELETE'])
# @permission_classes((IsAuthenticated, ))
# def RegisterClassId2(request, type_of_class, id):
#     if type_of_class == 'liveclass':
#         if request.method == 'GET':
#             try:
                
#                 registered_class = models.RegisteredClassNew.objects.create(conceptual_class_id=models.LiveClass_details.objects.get(id=id), user=request.user)
#                 registered_class.save()
#                 registered_live_class = models.LiveClass_details.objects.get(id=id)
#                 registered_live_class.no_of_students_registered += 1
#                 registered_live_class.save()
#             except Exception as e:
#                 return Response("Already registered")
        
#             return Response(status=status.HTTP_201_CREATED)

#         elif request.method == 'DELETE':

#             registered_class = models.RegisteredClassNew.objects.get(conceptual_class_id=models.LiveClass_details.objects.get(id=id), user=request.user)
#             registered_class.delete()
#             registered_live_class = models.LiveClass_details.objects.get(id=id)
#             registered_live_class.no_of_students_registered -= 1
#             registered_live_class.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)

#     elif type_of_class == 'doubtclass':
#         if request.method == 'GET':
#             try:
#                 registered_class = models.RegisteredClassNew.objects.create(doubtclass_id=models.DoubtClasses.objects.get(id=id), user=request.user)
#                 registered_class.save()
#                 registered_doubt_class = models.DoubtClasses.objects.get(id=id)
#                 registered_doubt_class.no_of_students_registered += 1
#                 registered_doubt_class.save()
#             except Exception as e:
#                 return Response("Already registered")
        
#             return Response(status=status.HTTP_201_CREATED)

#         elif request.method == 'DELETE':

#             registered_class = models.RegisteredClassNew.objects.get(doubtclass_id=models.DoubtClasses.objects.get(id=id), user=request.user)
#             registered_class.delete()
#             registered_doubt_class  = models.DoubtClasses.objects.get(id=id)
#             registered_doubt_class.no_of_students_registered -= 1
#             registered_doubt_class.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)

class RegisteredStudentsNames(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.RegisterNames_serializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        liveclass_id = models.LiveClass_details.objects.filter(id=self.kwargs['id']).first()
        print(liveclass_id)
        registered_students = liveclass_id.registered_students.all()
        return registered_students
        # return registered_students_id
    
    def get(self, request, id):
        if id:
            return self.list(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    
class RegisteredStudentsNamesdoubt(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.RegisterNames_serializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        liveclass_id = models.DoubtClasses.objects.filter(id=self.kwargs['id']).first()
        print(liveclass_id)
        registered_students = liveclass_id.registered_students.all()
        return registered_students
        # return registered_students_id
    
    def get(self, request, id):
        if id:
            return self.list(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

class AllChapterNames(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.ChapterNames_serializer
    permission_classes = [IsAuthenticated]
    queryset = models.ChapterNames.objects.all()
    # lookup_field = 'id'

    def get(self, request):
        return self.list(request)

import requests
import time

@csrf_exempt
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def GetZoomMeetings(request, type_of_class, id):

    if type_of_class == 'liveclass':
        try:
            liveclass = models.LiveClass_details.objects.get(id=id)
            if liveclass.meeting_id == '':
                return Response("zoom meeting has not been created for this class", status=status.HTTP_400_BAD_REQUEST)

            meeting_id = int(liveclass.meeting_id)
        except Exception as e:
            return Response("this class does not exists", status=status.HTTP_400_BAD_REQUEST)

    elif type_of_class == 'doubtclass':
        try:
            doubtclass = models.DoubtClasses.objects.get(id=id)
            if doubtclass.meeting_id == '':
                return Response("zoom meeting has not been created for this class", status=status.HTTP_400_BAD_REQUEST)
            meeting_id = int(doubtclass.meeting_id)
        except Exception as e:
            return Response("this class does not exists", status=status.HTTP_400_BAD_REQUEST)


    token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IldqOGFLU0lTUm5lNDhucnFCS3BPQlEiLCJleHAiOjE2MjY2NjI1NzQsImlhdCI6MTYyNjA1Nzc3NX0.rb55SRVcByMkr1Iy0D_lc7g041bWlbeCUFoMD8rGBgk'
    headers = {'authorization': 'Bearer %s' % token,
               'content-type': 'application/json'}
    print("error1")
    print(type(request.data))
    r = requests.get(
        f'https://api.zoom.us/v2/meetings/' + str(meeting_id), 
      headers=headers)
    return Response(r.json())
    


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def createZoomMeetings(request, type_of_class, id):

    # print(type(request.data))
    token = jwt.encode(
        
        # Create a payload of the token containing 
        # API Key & expiration time
        {'iss': credentials['API-KEY'], 'exp': time.time() + 5000},
          
        # Secret used to generate token signature
        credentials['API-SECRET'],
          
        # Specify the hashing alg
        algorithm='HS256'
    )
    # conn.request('POST', '/users/me/meetings/', headers=headers)
    # res = conn.getresponse()
    # data = res.read()
    # data = data.decode('utf8').replace("'", '"')
    # return Response(data)

      


    # payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
    #        'iss': credentials['API-KEY']
    #       }     
    # token = jwt.encode(payload, credentials['API-SECRET']).decode("utf-8")
    print(request.data)
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IldqOGFLU0lTUm5lNDhucnFCS3BPQlEiLCJleHAiOjE2MjY2NjI1NzQsImlhdCI6MTYyNjA1Nzc3NX0.rb55SRVcByMkr1Iy0D_lc7g041bWlbeCUFoMD8rGBgk'
    headers = {'authorization': 'Bearer %s' % token,
               'content-type': 'application/json'}
    print("error1")
    print(type(request.data))
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings', 
      headers=headers, data=json.dumps(request.data))
  
    print("\n creating zoom meeting ... \n")

    print(r.json())
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]

    if type_of_class == 'liveclass':
        liveclass = models.LiveClass_details.objects.get(id=id)
        print(liveclass)
        liveclass.meeting_url = join_URL
        liveclass.meeting_id = str(r.json()['id'])
        liveclass.save()
    if type_of_class == 'doubtclass':
        doubtclass = models.DoubtClasses.objects.get(id=id)
        doubtclass.meeting_url = join_URL
        doubtclass.meeting_id = str(r.json()['id'])
        doubtclass.save()
  
    return Response(r.json())
