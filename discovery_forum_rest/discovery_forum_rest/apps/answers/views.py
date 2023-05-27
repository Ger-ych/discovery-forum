from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Case, When, BooleanField

from rest_framework import generics, permissions, response, status, views

from questions.models import Question

from .models import Answer
from .serializers import AnswerListSerializer


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
