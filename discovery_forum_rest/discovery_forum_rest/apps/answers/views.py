from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Case, When, BooleanField

from rest_framework import generics, permissions, response, status, views

from questions.models import Question

from .models import Answer, AnswerComment
from .serializers import (
    AnswerListSerializer, 
    AnswerCommentListSerializer, 
    AnswerCreateSerializer,
    AnswerDetailSerializer, 
    AnswerCommentCreateSerializer
)
from questions.permissions import IsOwner

# list of answers
class AnswerListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = AnswerListSerializer

    def get_queryset(self):
        question_id = self.request.GET.get("question_id")
        question = get_object_or_404(Question, id=question_id)

        if self.request.user.is_authenticated:
            answers = Answer.objects.annotate(
                is_owner=Case(
                When(user=self.request.user, then=True),
                default=False,
                output_field=BooleanField(),
                )
            )

            answers = answers.filter(question=question).order_by(
                '-is_owner',
                '-is_solution',
                '-rating'
            )
        else:
            answers = Answer.objects.filter(question=question).order_by(
                '-is_solution',
                '-rating'
            )

        return answers

# list of answer comments
class AnswerCommentListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = AnswerCommentListSerializer

    def get_queryset(self):
        answer_id = self.request.GET.get("answer_id")
        answer = get_object_or_404(Answer, id=answer_id)
        comments = AnswerComment.objects.filter(answer=answer).order_by('-date_time')

        return comments

# answer create
class AnswerCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AnswerCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

# answer detail
class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Answer.objects.all()
    serializer_class = AnswerDetailSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

# answer comment create
class AnswerCommentCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AnswerCommentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
