

from django.urls import path, include

from . import views

urlpatterns = [
    path('questions/', views.QuestionModelView.as_view()),
    path('questions/<str:type_of_class>/class_id/<int:pk>', views.ClassBasedQuestions.as_view()),
    path('questions/<str:type_of_class>/', views.QuestionModelClass.as_view()),
    path('questions/<str:type_of_class>/<int:pk>/', views.QuestionModelViewID.as_view()),
    path('questions/<str:type_of_class>/put/<int:id>/', views.QuestionModelIDPut),
    # path('answers/<int:question_id>/', views.AnswerModel.as_view()),
    # path('answers/<int:question_id>/<int:pk>/', views.AnswerModelId.as_view())
]