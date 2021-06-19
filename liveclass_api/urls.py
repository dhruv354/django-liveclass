
from liveclass_api.models import RegisteredClass
from django.urls import path, include

from . import views

urlpatterns = [
    path('liveclass/', views.LiveClassView.as_view(), name='liveclass'),
     path('liveclass/<int:id>', views.LiveClassViewId.as_view()),
    path('mentors/', views.ListMentors.as_view(), name='mentors'),
    path('userdetails/', views.ListUserDetails.as_view(), name='user-details'),
    path('saved/', views.SavedClassView.as_view()),
    path('registerclass/', views.RegisterClass),
    path('registerclass/<int:id>/', views.RegisterClassId),
]