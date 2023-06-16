from django.db import models
from django.contrib.auth import get_user_model

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


# question category model
class QuestionCategory(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название категории")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория вопросов'
        verbose_name_plural = 'Категории вопросов'

# question model
class Question(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='questions',
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    heading = models.CharField(verbose_name="Заголовок", max_length=255)
    text = models.TextField(verbose_name="Текст")
    category = models.ForeignKey(
        QuestionCategory,
        related_name='questions',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    keywords = models.TextField(verbose_name="Ключевые слова", null=True, blank=True)
    following_users = models.ManyToManyField(
        get_user_model(),
        related_name="followed_questions",
        verbose_name="Отслеживающие пользователи",
        blank=True
    )
    date_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, auto_created=True, null=True, blank=True)
    
    def __str__(self):
        return f"Вопрос #{self.id}"  # type: ignore

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

# question comment model
class QuestionComment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='question_comments',
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    question = models.ForeignKey(
        Question,
        related_name='comments',
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    text = models.CharField(verbose_name="Текст", max_length=512)
    date_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, auto_created=True, null=True, blank=True)

    def __str__(self):
        return f"Комментарий #{self.id}" # type: ignore

    class Meta:
        verbose_name = 'Комментарий к вопросу'
        verbose_name_plural = 'Комментарии к вопросам'

@receiver(post_save, sender=QuestionComment)
def question_comment_notification(sender, instance, created, **kwargs):
    from notifications.models import Notification

    # creating a notification to the user when there is a new comment on a question
    if created:
        if instance.user != instance.question.user:
            if instance.user:
                text = f"Новый комментарий от пользователя {instance.user.username} к вашему вопросу \"{instance.question.heading}\": {instance.text}"
            else:
                text = f"Новый комментарий к вашему вопросу \"{instance.question.heading}\": {instance.text}"

            Notification.objects.create(
                user=instance.question.user,
                heading=f"Новый комментарий к вашему вопросу!",
                text=text,
                question=instance.question
            )
