from django.shortcuts import render
from . import models, serializers
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import status
from django.db.models import Q
import operator
# Create your views here.

class QuestionModelView(mixins.ListModelMixin, mixins.CreateModelMixin,GenericAPIView):
    queryset = models.QuestionModel.objects.all()
    serializer_class = serializers.QuestionModel_serializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class QuestionModelViewID(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,GenericAPIView):
    queryset = models.QuestionModel.objects.all()
    serializer_class = serializers.QuestionModel_serializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id=None):
        if int(request.POST.get('author')) != self.request.user.id:
            return Response("you cannot edit othe user question", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if id:
                return self.update(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
    def delete(self, request, id=None):
        if int(request.POST.get('author')) != self.request.user.id:
            return Response("you cannot destroy othe user question", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if id:
            return self.delete(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    
        


     
class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        q = reduce(operator.or_, (Q(x) for x in filter.items()))
        return get_object_or_404(queryset, q)


class AnswerModel(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    lookup_field = 'id'
    serializer_class = serializers.AnswerModel_serializer
   
    def get_queryset(self, *args, **kwargs):
        return models.AnswersModel.objects.filter(question_id = self.kwargs['id'])
    
    
    def get(self, request, id=None):
       return self.list(request)
      
    def post(self, request, id=None):
        if request.user.is_superuser:
            return self.create(request, id)
        else:
            return Response("only superuser can post a answer", status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, id=None)