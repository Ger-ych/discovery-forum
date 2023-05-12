from django.contrib import admin
from .models import Notification


# registration of notification model in administration
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "heading", "is_read", "date_time")

    fieldsets = (
        (None, {'fields': ('id', 'user', 'date_time', 'is_read')}),
        (None, {
            'fields': ('heading', 'text', 'link'),
        }),
    )

    readonly_fields = ('id', "date_time", )

    list_filter = ('user', 'is_read', 'date_time')

    save_on_top = True
