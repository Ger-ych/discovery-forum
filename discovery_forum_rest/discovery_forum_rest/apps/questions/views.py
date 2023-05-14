from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, response, status, views

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

# list of questions
class QuestionListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = QuestionListSerializer

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

    def get_queryset(self):
        username = self.request.GET.get("username")
        request = self.request

        if username:
            user = get_object_or_404(get_user_model(), username=username)
            questions = Question.objects.filter(user=user).order_by('-date_time')
        elif request.user.is_authenticated:
            questions = Question.objects.filter(user=request.user).order_by('-date_time')
        else:
            return None

        return questions

    def list(self, request, *args, **kwargs):
        # authorization check
        queryset = self.get_queryset()
        if queryset is None:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


# list of question comments
class QuestionCommentListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = QuestionCommentListSerializer

    def get_queryset(self):
        question_id = self.request.GET.get("question_id")
        question = get_object_or_404(Question, id=question_id)
        comments = QuestionComment.objects.filter(question=question).order_by('-date_time')

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

# question follow view
class QuestionFollowView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post']

    def post(self, request):
        question_id = request.data.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        user = request.user

        if user == question.user:
            return response.Response({'detail': 'Нельзя отслеживать свой же вопрос.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.followed_questions.filter(id=question.id).exists():
            user.followed_questions.remove(question)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            user.followed_questions.add(question)
            return response.Response(status=status.HTTP_201_CREATED)
