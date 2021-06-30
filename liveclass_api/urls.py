
from liveclass_api.models import RegisteredClass
from django.urls import path, include

from . import views

urlpatterns = [
    path('liveclass/', views.LiveClassView.as_view(), name='liveclass'),
    path('liveclass/<int:id>', views.LiveClassViewId.as_view()),
    path('liveclass/<int:id>/chapter-names', views.ChapterNames.as_view()),
    path('liveclass/<int:id>/registered-students', views.RegisteredStudentsNames.as_view()),
    path('mentors/', views.ListMentors.as_view(), name='mentors'),
    path('userdetails/', views.ListUserDetails.as_view(), name='user-details'),
    path('saved/', views.SavedClassView.as_view(), name='saved'),
    path('saved/<int:id>', views.SavedClassId),
    path('registerclass/', views.RegisterClass, name='registerclass'),
    path('registerclass/<int:id>/', views.RegisterClassId),
    path('registerclass/ratings/<int:id>', views.liveclassRatings),
    path('doubtclass/', views.DoubtClass.as_view(), name='doubtclass'),
    path('doubtclass/<int:id>', views.DoubtClassId.as_view()),
    path('drafts/', views.ListDrafts.as_view()),
    path('drafts/<int:id>', views.DraftClassId.as_view()),
    path('registerdoubtclass/', views.RegisterDoubtClass),
    path('registerdoubtclass/<int:id>/', views.RegisterDoubtClassId),
    path('registerdoubtclass/<int:id>/registered-students', views.RegisteredStudentsNamesdoubt),
    path('registerdoubtclass/ratings/<int:id>', views.DoubtclassRatings),
    # path('registerclass/<str:type_of_class>/<int:id>', views.RegisterClassId2),
    # path('registerclassnew/', views.RegisterClass2),
   
]