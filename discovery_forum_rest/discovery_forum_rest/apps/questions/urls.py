from django.urls import path
from .views import *

app_name = "questions"
urlpatterns = [
    path('categories/list/', QuestionCategoryListView.as_view()),

    path('list/', QuestionListView.as_view()),
    path('list/user/', UserQuestionListView.as_view()),
    path('detail/<int:id>/', QuestionDetailView.as_view()),
    path('create/', QuestionCreateView.as_view()),

    path('comments/list/', QuestionCommentListView.as_view()),
]
