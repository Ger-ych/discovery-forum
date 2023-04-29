from rest_framework import serializers
from .models import QuestionCategory, Question


# question category list serializer
class QuestionCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ('id', 'name')

# question category list serializer
class QuestionListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    correct_date_time = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return None
    
    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        else:
            return None
    
    def get_correct_date_time(self, obj):
        return obj.date_time.strftime("%m/%d/%Y %H:%M:%S")

    class Meta:
        model = Question
        fields = ('id', 'username', 'heading', 'category_name', 'correct_date_time')
