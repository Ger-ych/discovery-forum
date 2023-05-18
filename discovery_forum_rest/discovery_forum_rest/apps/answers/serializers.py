from rest_framework import serializers
from .models import Answer


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
