from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Question, QuestionComment
from answers.models import Answer, AnswerComment

from notifications.models import Notification
from notifications.serializers import (
    NotificationListSerializer
)


# notification create test
class NotificationCreateTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.other_user = get_user_model().objects.create(
            username='otheruser', email='other@example.com', password='otherpass'
        )
        self.question = Question.objects.create(
            user=self.user,
            heading='Question',
            text='Text', 
        )
        
    def test_create_answer_notification(self):
        answer = Answer.objects.create(
            user=self.other_user,
            question=self.question,
            heading="Answer",
            text="Text"
        )
        notification = Notification.objects.last()
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.question, answer.question)

    def test_set_solution_answer_notification(self):
        answer = Answer.objects.create(
            user=self.other_user,
            question=self.question,
            heading="Answer",
            text="Text"
        )

        answer.is_solution = True
        answer.save()
        notification = Notification.objects.last()
        self.assertEqual(notification.user, answer.user)
        self.assertEqual(notification.question, answer.question)

    def test_create_answer_comment_notification(self):
        answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            heading="Answer",
            text="Text"
        )
        answer_comment = AnswerComment.objects.create(
            user=self.other_user,
            answer=answer,
            text="Comment"
        )
        notification = Notification.objects.last()
        self.assertEqual(notification.user, answer.user)
        self.assertEqual(notification.question, answer_comment.answer.question)

    def test_create_question_comment_notification(self):
        question_comment = QuestionComment.objects.create(
            user=self.other_user,
            question=self.question,
            text="Comment"
        )
        notification = Notification.objects.last()
        self.assertEqual(notification.user, question_comment.question.user)
        self.assertEqual(notification.question, question_comment.question)

# notification list test
class NotificationListViewTestCase(APITestCase):
    def setUp(self): 
        self.url_get_count_unread = reverse('notifications:notification_get_count_unread')
        self.url_list = reverse('notifications:notification_list')
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.question = Question.objects.create(
            user=self.user,
            heading='Question',
            text='Text', 
        )     
        self.notification1 = Notification.objects.create(
            user=self.user,
            heading="Notification 1",
            text="Text",
            question=self.question
        )
        self.notification2 = Notification.objects.create(
            user=self.user,
            heading="Notification 2",
            text="Text",
            question=self.question,
            is_read=True
        )
        
    def test_notification_list(self):
        self.client.force_login(user=self.user)

        response = self.client.get(self.url_get_count_unread)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), len(Notification.objects.filter(user=self.user, is_read=False)))

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Notification.objects.filter(user=self.user, is_read=False))
