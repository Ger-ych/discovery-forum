# Generated by Django 4.0.3 on 2023-04-26 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('answers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(choices=[(2, 'Ответ полезен'), (-1, 'Бесполезный ответ'), (1, 'Ответ релевантен')], max_length=128, verbose_name='Оценка')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='answers.answer', verbose_name='Ответ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_rates', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Оценка ответа',
                'verbose_name_plural': 'Оценки ответов',
            },
        ),
    ]
