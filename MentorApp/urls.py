

from django.urls import path, include

from . import views

urlpatterns = [
    path('questions/', views.QuestionModelView.as_view()),
    path('questions/<int:id>/', views.QuestionModelViewID.as_view()),
    path('questions/<int:id>/answer/', views.AnswerModel.as_view()),
    path('questions/<int:question_id>/answer/<int:answer_id>', views.AnswerModelID)
]