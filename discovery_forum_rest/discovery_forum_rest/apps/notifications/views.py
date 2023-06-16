from rest_framework import generics, permissions, response, status, views

from .models import Notification
from .serializers import NotificationListSerializer


# list of notifications
class NotificationListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NotificationListSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-is_read')
