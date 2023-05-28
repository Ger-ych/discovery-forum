from rest_framework import serializers
from .models import Answer, AnswerComment


# answer list serializer
class AnswerListSerializer(serializers.ModelSerializer):
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
        model = Answer
        fields = ('id', 'username', 'heading', 'text', 'is_solution', 'rating', 'correct_date_time')

# amswer comment list serializer
class AnswerCommentListSerializer(serializers.ModelSerializer):
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
        model = AnswerComment
        fields = ('id', 'username', 'text', 'correct_date_time')

# answer create serializer
class AnswerCreateSerializer(serializers.ModelSerializer):
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
        model = Answer
        fields = ('id', 'username', 'question', 'heading', 'text', 'is_solution', 'correct_date_time')
        
        read_only_fields = ('id', 'username', 'is_solution', 'correct_date_time')
        read_write_fields = ('question', 'heading', 'text')
