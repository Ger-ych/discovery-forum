from rest_framework import serializers
from .models import QuestionCategory


# question category list serializer
class QuestionCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ('id', 'name')
