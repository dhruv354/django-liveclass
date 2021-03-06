from django.shortcuts import render
from . import models, serializers
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from liveclass_api import models as liveclass_models
from liveclass_api import serializers as liveclass_serializers
import json
from django.shortcuts import get_object_or_404
from django.http import QueryDict


# Create your views here.


class MultipleFieldLookupORMixin(object):
    """
    Actual code http://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            try:                                  # Get the result with one or more fields.
                filter[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter)  # Lookup the object

class QuestionUpdateMixin:
    """
    Question Update View Mixin
    """
    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.is_superuser: # or any other condition
            self.fields = [
                'answer',
            ]
        else:
            self.fields = [
                'doubt_class_id', 'conceptual_class_id', 'mentor', 'question',
            ]

        return super().dispatch(request, pk, *args, **kwargs)  


class QuestionModelView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.QuestionModel.objects.all()
    serializer_class = serializers.QuestionModel_serializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)
# 




class QuestionModelClass(mixins.ListModelMixin, mixins.CreateModelMixin,  GenericAPIView):
    # queryset = models.QuestionModel.objects.filter(doubt_class_id__isnull = False)
    serializer_class = serializers.QuestionModel_serializer
    lookup_field = 'type_of_class'
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        # print('error here')
        if self.kwargs['type_of_class'] == 'doubtclass':
            return models.QuestionModel.objects.filter(doubt_class_id__isnull = False)
        elif self.kwargs['type_of_class'] == 'liveclass':
            return models.QuestionModel.objects.filter(conceptual_class_id__isnull = False)
    
    def get(self, request, type_of_class=None):
        return self.list(request, type_of_class)

    def post(self, request, type_of_class=None):
        if int(request.data.get('author')) != self.request.user.id:
            return Response("you cannot create for any  other user question", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return self.create(request, type_of_class)


# def QuestionModelId(request, type_of_class):
#     if type_of_class == 'doubtclass':
#         doubt_classes = models.QuestionModel.objects.filter(doubt_class_id__isnull = False)
#         if request.method == 'GET':
#             serializer = serializers.QuestionModel_serializer(doubt_classes, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         if request.method == 'POST':
#             body_data = json.loads(request.body)
#             author_id = body_data['author']
#             if author_id != request.user.id:
#                 return Response("you cannot edit othe user question", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
#             serializer = serializers.QuestionModel_serializer(doubt_classes, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif type_of_class == 'liveclass':
#         conceptual_classes = models.QuestionModel.objects.filter(conceptual_class_id__isnull = False)
#         if request.method == 'GET':
#             serializer = serializers.QuestionModel_serializer(conceptual_classes, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         if request.method == 'POST':
#             if int(request.body('author')) != request.user.id:
#                 return Response("you cannot edit othe user question", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
#             serializer = serializers.QuestionModel_serializer(conceptual_classes, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class QuestionModelViewID(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, GenericAPIView):
    serializer_class = serializers.QuestionModel_serializer
    permission_classes = [IsAuthenticated]
    lookup_fields = ('type_of_class', 'pk')
    def get_queryset(self):
        print(self.kwargs['type_of_class'])
        type_of_class = self.kwargs['type_of_class']
        if type_of_class == 'doubtclass':
            print('error here')
            return models.QuestionModel.objects.filter(id=self.kwargs['pk'])
        elif type_of_class == 'liveclass':
            return models.QuestionModel.objects.filter(id=self.kwargs['pk'])
    def get(self, request,type_of_class ,pk=None):
        print('error here')
        if pk:
            return self.list(request, type_of_class, pk)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # s
        # if pk:
        #     question_id = models.QuestionModel.objects.filter(id=pk).first()
            #if answer originally exists
            # print(question_id.answer)
            # print(request.user.is_superuser)
            # if len(question_id.answer) > 0:
            #     self.update(request, type_of_class, pk)
            #     #self.update(request, type_of_class, pk)
            #     if len(question_id.answer) > 0 :
            #         return Response("Successfully updated answer", status=status.HTTP_200_OK)
            #     # this means that answer is deleted so decrease doubt address count
            #     else:
            #         if type_of_class =='doubtclass':
            #             class_id = question_id.doubt_class_id
            #         elif type_of_class == 'liveclass':
            #             class_id = question_id.conceptual_class_id
            #         class_id.doubtsAddressed -= 1
            #         class_id.save()
            #         return Response("Successfully deleted answer", status=status.HTTP_200_OK)

            #if answer is not originally there
        #     self.update(request, type_of_class, pk)
        #     #this means that a student has updated his answer
        #     if question_id.answer == '':
        #         return Response("successfully updated a question", status=status.HTTP_200_OK)
        #     #this means that a mentor has posted a answer
        #     if type_of_class =='doubtclass':
        #         print("type_of_class =='doubtclass'")
        #         class_id = question_id.doubt_class_id
        #     elif type_of_class == 'liveclass':
        #         print("type_of_class =='conceptual_class'")
        #         class_id = question_id.conceptual_class_id
        #         print(class_id)
        #     class_id.doubtsAddressed += 1
        #     class_id.save()
        #     return Response("Successfully posted answer", status=status.HTTP_200_OK)

        # else:
        #     return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, type_of_class=None, pk=None):
        author_id = models.QuestionModel.objects.filter(id=pk).values('author_id').first()['author_id']
        if int(author_id)!= self.request.user.id:
            return Response("you cannot delete othe user question", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if pk:
                return self.destroy(request, type_of_class, pk)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        




@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))

def QuestionModelIDPut(request, type_of_class, id):
        try:
            question_id = models.QuestionModel.objects.filter(id=id).first()
            if type_of_class =='doubtclass':
                class_id = question_id.doubt_class_id
            elif type_of_class == 'liveclass':
                class_id = question_id.conceptual_class_id
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.QuestionModel_serializer(question_id, request.data)
        initial_answer_length = len(question_id.answer)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if initial_answer_length == 0:
            print("initial length is 0")
            serializer.save()
            question = models.QuestionModel.objects.filter(id=id).first()
            if len(question.answer) == 0:
                print("initial length still zero")
                return Response("please post a answer")
            else:
                print("posted  a new answer")
                class_id.doubtsAddressed += 1
                class_id.save()
                return Response(serializer.data)
        else:
            serializer.save()
            question = models.QuestionModel.objects.filter(id=id).first()
            print("initial length non zer0")
            if len(question.answer) == 0:
                print("final length has become zero")
                class_id.doubtsAddressed -= 1
                class_id.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                print("final length is also non zero")
                return Response(serializer.data, status=status.HTTP_200_OK)



        










class AnswerModel(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    lookup_field = 'question_id'
    serializer_class = serializers.AnswerModel_serializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):
        try:
            return models.AnswersModel.objects.filter(question_id = self.kwargs['question_id'])
        except Exception as e:
            print(e)
            return Response("such question with this id does not exists", status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, question_id=None):
        question = models.QuestionModel.objects.filter(id=question_id).first()

        return self.list(request, question_id)
      
    def post(self, request, question_id=None):
        if not question_id:
           return Response("no such question with this id", status=status.HTTP_404_NOT_FOUND)
        if request.user.is_superuser:
            return self.create(request, question_id)
        else:
            return Response("only superuser can post a answer", status=status.HTTP_400_BAD_REQUEST)
    
    


# @api_view(['PUT', 'DELETE'])
# @permission_classes((IsAuthenticated, ))

# def AnswerModelID(request, question_id, answer_id):
    
#     answers_particular_question = models.AnswersModel.objects.filter(question_id = question_id)
#     particular_answer = answers_particular_question.filter(id=answer_id)

#     if request.method == 'PUT':
#         if request.user.is_superuser:
#             serializer = serializers.AnswerModel_serializer(particular_answer, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         else:
# #             return Response("only for mentors", status=status.HTTP_401_UNAUTHORIZED)
    
# #     elif request.method == 'DELETE':
# #         if request.user.is_auperuser:
# #             particular_answer.delete()
# #             return Response(status=status.HTTP_204_NO_CONTENT)


# class AnswerModelId(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
#     serializer_class = serializers.AnswerModel_serializer
#     lookup_fields = ('question_id', 'pk')
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return models.AnswersModel.objects.filter(id=self.kwargs['pk'])

#     def get(self, request, question_id=None, pk=None):
#         if pk and question_id:
#             return self.retrieve(request, question_id, pk)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, question_id=None, pk=None):
#         if request.is_superuser:
#             if pk and question_id:
#                 return self.put(request, question_id, pk)
#             else:
#                 return Response(status=status.HTTP_404_NOT_FOUND)
#         return Response("you cannot update this question", status=status.HTTP_401_UNAUTHORIZED)

#     def delete(self, request, question_id=None, pk=None):
#         if request.is_superuser:
#             if question_id and pk:
#                 return self.destroy(request, question_id, pk)
#             else:
#                 return Response(status=status.HTTP_404_NOT_FOUND)
#         return Response("you cannot update this question", status=status.HTTP_401_UNAUTHORIZED)

    
class ClassBasedQuestions(mixins.ListModelMixin, GenericAPIView):

    serializer_class = serializers.QuestionModel_serializer
    lookup_fields = ('type_of_class', 'pk')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        type_of_class = self.kwargs['type_of_class']
        pk = self.kwargs['pk']
        if type_of_class == 'doubtclass':
            return models.QuestionModel.objects.filter(doubt_class_id=pk)
        elif type_of_class == 'liveclass':
            return models.QuestionModel.objects.filter(conceptual_class_id = pk)
    
    def get(self, request, type_of_class=None, pk=None):
        if pk:
            return self.list(request, type_of_class, pk)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)