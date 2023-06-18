from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from questions.models import Question
from notifications.models import Notification

from .utils import calc_answer_rating


# answer model
class Answer(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='answers',
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    question = models.ForeignKey(
        Question,
        related_name='answers',
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    heading = models.CharField(verbose_name="Заголовок", max_length=255)
    text = models.TextField(verbose_name="Текст")
    is_solution = models.BooleanField(default=False, verbose_name="Решение вопроса")
    was_solution = models.BooleanField(default=False)
    date_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, auto_created=True, null=True, blank=True)
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    
    def __str__(self):
        return f"Ответ #{self.id}" # type: ignore

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

@receiver(post_save, sender=Answer)
def answer_notification(sender, instance, created, **kwargs):
    # creating a notification to the user when creating an answer to a question
    if created:
        heading = "Новый ответ на вопрос!"
        text = f"Новый ответ на вопрос \"{instance.question.heading}\": {instance.heading}"
        question = instance.question

        if instance.question.user and instance.user != instance.question.user:
            Notification.objects.create(
                user=instance.question.user,
                heading=heading,
                text=text,
                question=question
            )
        for u in instance.question.following_users.all():
            if u != instance.user:
                Notification.objects.create(
                    user=u,
                    heading=heading,
                    text=text,
                    question=question
                )
    
    # creating a notification to the user when his answer is marked as a solution
    if instance.is_solution != instance.was_solution:
        if instance.is_solution and instance.user:
            Notification.objects.create(
                user=instance.user,
                heading="Ваш ответ помечен, как решение!",
                text=f"Ваш ответ \"{instance.heading}\" на вопрос \"{instance.question.heading}\" помечен, как решение.",
                question=instance.question
            )

        instance.was_solution = instance.is_solution
        instance.save()

# answer comment model
class AnswerComment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='answer_comments',
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    answer = models.ForeignKey(
        Answer,
        related_name='comments',
        verbose_name='Ответ',
        on_delete=models.CASCADE,
    )
    text = models.CharField(verbose_name="Текст", max_length=512)
    date_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, auto_created=True, null=True, blank=True)

    def __str__(self):
        return f"Комментарий #{self.id}" # type: ignore

    class Meta:
        verbose_name = 'Комментарий к ответу'
        verbose_name_plural = 'Комментарии к ответу'

@receiver(post_save, sender=AnswerComment)
def answer_comment_notification(sender, instance, created, **kwargs):
    # creating a notification to the user when there is a new comment on a answer
    if created:
        if instance.user != instance.answer.user and instance.answer.user:
            if instance.user:
                text = f"Новый комментарий от пользователя {instance.user.username} к вашему ответу \"{instance.answer.heading}\" по вопросу \"{instance.answer.question.heading}\": {instance.text}"
            else:
                text = f"Новый комментарий к вашему ответу \"{instance.answer.heading}\" по вопросу \"{instance.answer.question.heading}\": {instance.text}"

            Notification.objects.create(
                user=instance.answer.user,
                heading=f"Новый комментарий к вашему ответу!",
                text=text,
                question=instance.answer.question
            )

# answer rate model
class AnswerRate(models.Model):
    # answer rate choices
    RATE_USEFUL = 2
    RATE_USELESS = -1
    RATE_RELEVANT = 1
    RATE_CHOICES = [
        (RATE_USEFUL, 'Ответ полезен'),
        (RATE_USELESS, 'Бесполезный ответ'),
        (RATE_RELEVANT, 'Ответ релевантен'),
    ]

    user = models.ForeignKey(
        get_user_model(),
        related_name='answer_rates',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        Answer,
        related_name='rates',
        verbose_name='Ответ',
        on_delete=models.CASCADE,
    )
    rate = models.IntegerField(verbose_name='Оценка', choices=RATE_CHOICES)

    def __str__(self):
        return self.get_rate_display() # type: ignore

    class Meta:
        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответов'

# calculation of answer rating by rates
@receiver(post_save, sender=AnswerRate)
def answer_rating_save(sender, instance, created, **kwargs):
    calc_answer_rating(instance.answer)

@receiver(post_delete, sender=AnswerRate)
def answer_rating_delete(sender, instance, **kwargs):
    calc_answer_rating(instance.answer)
