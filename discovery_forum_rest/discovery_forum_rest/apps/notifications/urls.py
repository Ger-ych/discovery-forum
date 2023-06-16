from django.urls import path
from .views import *

app_name = "notifications"
urlpatterns = [
    path('list/', NotificationListView.as_view(), name='notification_list'),
    path('get/count/unread/', GetCountUnreadView.as_view(), name='notification_get_count_unread'),
]
