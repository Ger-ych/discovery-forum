from django.urls import path
from .views import *

app_name = "questions"
urlpatterns = [
    path('categories/list/', QuestionCategoryListView.as_view()),
    path('list/', QuestionListView.as_view()),
    path('list/user/', UserQuestionListView.as_view()),
]
