from django.shortcuts import render
from rest_framework import generics, permissions

from .models import QuestionCategory
from .serializers import QuestionCategoryListSerializer

# list of question categories
class QuestionCategoryListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = QuestionCategoryListSerializer
    queryset = QuestionCategory.objects.all()
    http_method_names = ['get', ]
