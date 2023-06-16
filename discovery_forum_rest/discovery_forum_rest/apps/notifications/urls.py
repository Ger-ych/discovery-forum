from django.urls import path
from .views import *

app_name = "notifications"
urlpatterns = [
    path('list/', NotificationListView.as_view(), name='notification_list'),
]
