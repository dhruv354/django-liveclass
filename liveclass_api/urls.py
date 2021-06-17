
from django.urls import path, include
from . import views

urlpatterns = [
    path('liveclass/', views.ListLiveClass.as_view()),
    path('mentors/', views.ListMentors.as_view())
]