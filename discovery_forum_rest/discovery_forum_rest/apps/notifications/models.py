from django.db import models
from django.contrib.auth import get_user_model


# notification model
class Notification(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='notifications',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    heading = models.CharField(verbose_name="Заголовок", max_length=255)
    text = models.TextField(verbose_name="Текст")
    link = models.TextField(verbose_name="Ссылка")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    date_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, auto_created=True, null=True, blank=True)
    
    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
