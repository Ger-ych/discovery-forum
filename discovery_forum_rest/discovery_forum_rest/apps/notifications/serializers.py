from rest_framework import serializers
from .models import Notification


# notification list serializer
class NotificationListSerializer(serializers.ModelSerializer):
    correct_date_time = serializers.SerializerMethodField()
    
    def get_correct_date_time(self, obj):
        return obj.date_time.strftime("%m/%d/%Y %H:%M:%S")

    class Meta:
        model = Notification
        fields = ('id', 'heading', 'text', 'is_read', 'correct_date_time')
