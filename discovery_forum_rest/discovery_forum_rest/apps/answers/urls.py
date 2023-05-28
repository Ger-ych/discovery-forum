from django.urls import path
from .views import *

app_name = "answers"
urlpatterns = [
    path('list/', AnswerListView.as_view(), name='answer_list'),
    path('create/', AnswerCreateView.as_view(), name='answer_create'),

    path('comments/list/', AnswerCommentListView.as_view(), name='comment_list'),
]
