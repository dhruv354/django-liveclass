from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
# from .models import Profile

# Create your views here.

# def register(request):

#     if request.method == 'POST':
#         form = MyRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'successfully created account for {username}')
#             return redirect('login')
#         else:
#             print('some error')
#     else:
#         form = MyRegisterForm()
#     return render(request, 'authentication/register.html', {'form': form})




@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# class current_user(mixins.ListModelMixin, GenericAPIView):
#     serializer_class = UserSerializer()
#     def get(self, request):
#         return self.list(request)


class UserList(mixins.CreateModelMixin, GenericAPIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializerWithToken

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''To be constructed'''

class Logout(APIView):
    pass