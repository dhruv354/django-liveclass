
from django.urls import path, include

from . import views

urlpatterns = [
    path('liveclass/', views.LiveClassView.as_view(), name='liveclass'),
     path('liveclass/<int:id>', views.LiveClassViewId.as_view()),
    path('mentors/', views.ListMentors.as_view(), name='mentors'),
    path('userdetails/', views.ListUserDetails.as_view(), name='user-details'),
]