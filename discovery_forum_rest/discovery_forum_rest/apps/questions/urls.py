from django.urls import path
from .views import *

app_name = "questions"
urlpatterns = [
    path('categories/list/', QuestionCategoryListView.as_view(), name='category_list'),

    path('list/', QuestionListView.as_view(), name='question_list'),
    path('list/user/', UserQuestionListView.as_view(), name='question_user_list'),
    path('detail/<int:id>/', QuestionDetailView.as_view(), name='question_detail'),
    path('create/', QuestionCreateView.as_view(), name='question_create'),
    path('follow/', QuestionFollowView.as_view(), name='question_follow'),

    path('comments/list/', QuestionCommentListView.as_view(), name='comment_list'),
    path('comments/create/', QuestionCommentCreateView.as_view(), name='comment_create'),
    path('comments/detail/<int:id>/', QuestionCommentDetailView.as_view(), name='comment_detail'),
]
