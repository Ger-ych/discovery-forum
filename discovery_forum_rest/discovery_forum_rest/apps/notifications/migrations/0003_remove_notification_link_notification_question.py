# Generated by Django 4.2.2 on 2023-06-15 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_alter_question_following_users'),
        ('notifications', '0002_alter_notification_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='link',
        ),
        migrations.AddField(
            model_name='notification',
            name='question',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='question_notifications', to='questions.question', verbose_name='Вопрос'),
            preserve_default=False,
        ),
    ]
