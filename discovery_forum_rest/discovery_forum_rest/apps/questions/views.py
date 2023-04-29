from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from .models import QuestionCategory, Question
from .serializers import QuestionCategoryListSerializer, QuestionListSerializer


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
        keywords = self.request.GET.get("keywords")

        questions = Question.objects.order_by('-date_time')

        if category_id:
            questions = questions.filter(category=get_object_or_404(QuestionCategory, id=category_id))

        # TODO searching questions by query and keywords
        
        return questions
