from django.urls import path
from .views import *

app_name = "answers"
urlpatterns = [
    path('list/', AnswerListView.as_view(), name='answer_list'),
    path('create/', AnswerCreateView.as_view(), name='answer_create'),
    path('detail/<int:id>/', AnswerDetailView.as_view(), name='answer_detail'),

    path('comments/list/', AnswerCommentListView.as_view(), name='comment_list'),
    path('comments/create/', AnswerCommentCreateView.as_view(), name='comment_create'),
    path('comments/detail/<int:id>/', AnswerCommentDetailView.as_view(), name='comment_detail'),
]
