from rest_framework import generics, permissions, response, status, views

from .models import Notification
from .serializers import NotificationListSerializer


# list of notifications
class NotificationListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NotificationListSerializer

    def get_queryset(self):
        notifications = Notification.objects.filter(user=self.request.user).order_by('-is_read')
        notifications.update(is_read=True)

        return notifications

# getting the number of unread notifications
class GetCountUnreadView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get',]

    def get(self, request):
        count = len(Notification.objects.filter(user=self.request.user, is_read=False))
        return response.Response(data={"count": count}, status=status.HTTP_200_OK)
