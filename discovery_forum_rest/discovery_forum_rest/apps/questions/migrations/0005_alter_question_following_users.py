# Generated by Django 4.0.3 on 2023-04-26 12:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0004_alter_question_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='following_users',
            field=models.ManyToManyField(blank=True, related_name='followed_questions', to=settings.AUTH_USER_MODEL, verbose_name='Отслеживающие пользователи'),
        ),
    ]
