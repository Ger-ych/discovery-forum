# Generated by Django 4.0.3 on 2023-04-25 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0003_alter_question_following_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='questions.questioncategory', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='question',
            name='following_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='followed_questions', to=settings.AUTH_USER_MODEL, verbose_name='Отслеживающие пользователи'),
        ),
        migrations.AlterField(
            model_name='question',
            name='keywords',
            field=models.TextField(blank=True, null=True, verbose_name='Ключевые слова'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='questions.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_comments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
