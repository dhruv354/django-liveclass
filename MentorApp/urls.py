

from django.urls import path, include

from . import views

urlpatterns = [
    path('questions/', views.QuestionModelView.as_view()),
<<<<<<< HEAD
    path('questions/type_of_class/class_id/<int:pk>', views.ClassBasedQuestions.as_view()),
=======
    path('questions/class/<str:type_of_class>/<int:pk>', views.ClassBasedQuestions.as_view()),
>>>>>>> baa7c71272e31124a6e8134d3246ada4e0ebb9b0
    path('questions/<str:type_of_class>/', views.QuestionModelClass.as_view()),
    path('questions/<str:type_of_class>/<int:pk>/', views.QuestionModelViewID.as_view()),
    # path('answers/<int:question_id>/', views.AnswerModel.as_view()),
    # path('answers/<int:question_id>/<int:pk>/', views.AnswerModelId.as_view())
]