from django.shortcuts import render
from . import models, serializers
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import status
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

        if id:
                return self.update(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
    def delete(self, request, id=None):
        if id:
            return self.delete(request, id)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    
        from django.shortcuts import render

# Create your views here.
