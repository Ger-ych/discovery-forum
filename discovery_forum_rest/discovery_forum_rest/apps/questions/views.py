from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, response

from .models import QuestionCategory, Question, QuestionComment
from .serializers import (
    QuestionCategoryListSerializer, 
    QuestionListSerializer, 
    QuestionCommentListSerializer, 
    QuestionDetailSerializer, 
    QuestionCreateSerializer, 
    QuestionCommentCreateSerializer, 
    QuestionCommentDetailSerializer
)
from .permissions import IsOwner


# list of question categories
class QuestionCategoryListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = QuestionCategoryListSerializer
    queryset = QuestionCategory.objects.all()
    http_method_names = ['get', ]

# list of questions
class QuestionListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = QuestionListSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        category_id = self.request.GET.get("category_id")
        query = self.request.GET.get("q")

        questions = Question.objects.order_by('-date_time')

        if category_id:
            questions = questions.filter(category=get_object_or_404(QuestionCategory, id=category_id))
        
        if query:
            questions = questions.filter(heading__icontains=query)

        return questions

# list of user questions
class UserQuestionListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = QuestionListSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        username = self.request.GET.get("username")
        request = self.request

        if username:
            questions = Question.objects.filter(user=get_object_or_404(get_user_model(), username=username)).order_by('-date_time')
        elif request.user.is_authenticated:
            questions = Question.objects.filter(user=request.user).order_by('-date_time')
        else:
            return response.Response(status=401)

        return questions


# list of question comments
class QuestionCommentListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = QuestionCommentListSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        question_id = self.request.GET.get("question_id")
        comments = QuestionComment.objects.filter(question=get_object_or_404(Question, id=question_id)).order_by('-date_time')

        return comments

# question create
class QuestionCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = QuestionCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

# question detail
class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

# question comment create
class QuestionCommentCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = QuestionCommentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

# question comment detail
class QuestionCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = QuestionComment.objects.all()
    serializer_class = QuestionCommentDetailSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
