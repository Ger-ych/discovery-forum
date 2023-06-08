from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Case, When, BooleanField

from rest_framework import generics, permissions, response, status, views

from questions.models import Question

from .models import Answer, AnswerComment, AnswerRate
from .serializers import (
    AnswerListSerializer, 
    AnswerCommentListSerializer, 
    AnswerCreateSerializer,
    AnswerDetailSerializer, 
    AnswerCommentCreateSerializer, 
    AnswerCommentDetailSerializer,
    UserAnswerRateSerializer
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

# answer comment detail
class AnswerCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = AnswerComment.objects.all()
    serializer_class = AnswerCommentDetailSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

# answer set solution
class AnswerSetSolutionView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post']

    def post(self, request):
        answer_id = request.data.get('answer')
        answer = get_object_or_404(Answer, id=answer_id)
        question = answer.question

        user = request.user     

        if user != question.user:
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        if answer.is_solution:
            answer.is_solution = False
        else:
            answer.is_solution = True

        answer.save()

        return response.Response(data={"is_solution": answer.is_solution}, status=status.HTTP_200_OK)

# answer rate list
class AnswerRateListView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']

    def get(self, request):
        return response.Response(data=AnswerRate.RATE_CHOICES, status=status.HTTP_200_OK)

# user answer rate
class UserAnswerRateView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserAnswerRateSerializer

    def get_object(self):
        user = self.request.user

        answer_id = self.request.GET.get('answer_id')
        answer = get_object_or_404(Answer, id=answer_id)
        
        return get_object_or_404(AnswerRate, user=user, answer=answer)

# answer rate create
class AnswerRateCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user

        rate = int(request.data.get('rate'))
        valid_rates = [x[0] for x in AnswerRate.RATE_CHOICES]
        if not rate in valid_rates:
            return response.Response(data={"rate": [f"Недопустисое значение \"{rate}\"."]}, status=status.HTTP_400_BAD_REQUEST)

        answer_id = request.data.get('answer')
        answer = get_object_or_404(Answer, id=answer_id)
        
        if AnswerRate.objects.filter(answer=answer, user=user).exists():
            answer_rate = AnswerRate.objects.filter(answer=answer, user=user).first()
            if answer_rate.rate == rate:
                answer_rate.delete()
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            else:
                answer_rate.rate = rate
                answer_rate.save()
                return response.Response(status=status.HTTP_200_OK)
        else:
            AnswerRate.objects.create(answer=answer, user=user, rate=rate)
            return response.Response(status=status.HTTP_201_CREATED)
