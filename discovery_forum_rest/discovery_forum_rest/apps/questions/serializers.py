from rest_framework import serializers
from .models import QuestionCategory, Question, QuestionComment


# question category list serializer
class QuestionCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ('id', 'name')

# question list serializer
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
        fields = ('id', 'username', 'heading', 'category_name', 'category', 'correct_date_time')

# question comment list serializer
class QuestionCommentListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    correct_date_time = serializers.SerializerMethodField()

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return None

    def get_correct_date_time(self, obj):
        return obj.date_time.strftime("%m/%d/%Y %H:%M:%S")

    class Meta:
        model = QuestionComment
        fields = ('id', 'username', 'text', 'correct_date_time')

# question create serializer
class QuestionCreateSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'username', 'heading', 'text', 'category_name', 'category', 'keywords', 'correct_date_time')
        
        read_only_fields = ('id', 'username', 'category_name', 'correct_date_time')
        read_write_fields = ('heading', 'text', 'category', 'keywords')

# question detail serializer
class QuestionDetailSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'username', 'heading', 'text', 'category_name', 'category', 'keywords', 'correct_date_time')
        
        read_only_fields = ('id', 'username', 'category_name', 'correct_date_time')
        read_write_fields = ('heading', 'text', 'category', 'keywords')

# question create serializer
class QuestionCommentCreateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    correct_date_time = serializers.SerializerMethodField()

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return None

    def get_correct_date_time(self, obj):
        return obj.date_time.strftime("%m/%d/%Y %H:%M:%S")

    class Meta:
        model = QuestionComment
        fields = ('id', 'username', 'question', 'text', 'correct_date_time')
        
        read_only_fields = ('id', 'username', 'correct_date_time')
        read_write_fields = ('question', 'text')

# question comment detail serializer
class QuestionCommentDetailSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    correct_date_time = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return None
    
    def get_correct_date_time(self, obj):
        return obj.date_time.strftime("%m/%d/%Y %H:%M:%S")

    class Meta:
        model = QuestionComment
        fields = ('id', 'username', 'question', 'text', 'correct_date_time')
        
        read_only_fields = ('id', 'username', 'question', 'correct_date_time')
        read_write_fields = ('text',)
