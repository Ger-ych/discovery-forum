from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Question

from answers.models import Answer, AnswerComment, AnswerRate
from answers.serializers import (
    AnswerCreateSerializer,
    AnswerDetailSerializer,
    AnswerCommentCreateSerializer,
    AnswerCommentDetailSerializer
)

# answer list test
class AnswerListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('answers:answer_list')

        self.question = Question.objects.create(
            heading='Question',
            text='Text',
        )
        self.answer1 = Answer.objects.create(
            question=self.question,
            heading='Answer 1',
            text='Text 1'
        )
        self.answer2 = Answer.objects.create(
            question=self.question,
            heading='Answer 2',
            text='Text 2'
        )

    def test_get_answers(self):
        response = self.client.get(self.url, {"question_id": self.question.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# answer comment list test
class AnswerCommentListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('answers:comment_list')

        self.question = Question.objects.create(
            heading='Question',
            text='Text',
        )
        self.answer = Answer.objects.create(
            question=self.question,
            heading='Answer',
            text='Text'
        )
        self.comment1 = AnswerComment.objects.create(
            text='Comment 1',
            answer=self.answer
        )
        self.comment2 = AnswerComment.objects.create(
            text='Comment 2',
            answer=self.answer
        )
        
    def test_get_answers(self):
        response = self.client.get(self.url, {"answer_id": self.answer.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# answer create test
class AnswerCreateViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("answers:answer_create")

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.question = Question.objects.create(
            heading='Question',
            text='Text',
        )
        self.create_data = {
            "question": self.question.id,
            "heading": "Answer",
            "text": "Text",
        }

    def test_create_answer(self):
        self.client.force_login(user=self.user)

        response = self.client.post(self.url, self.create_data)
        answer = Answer.objects.last()
        serializer = AnswerCreateSerializer(answer)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data) # type: ignore
        self.assertEqual(answer.user, self.user) # type: ignore

    def test_create_answer_unauthenticated(self):
        response = self.client.post(self.url, self.create_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Answer.objects.exists())


# answer detail test
class AnswerDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.other_user = get_user_model().objects.create(
            username='otheruser', email='other@example.com', password='otherpass'
        )
        self.question = Question.objects.create(
            heading='Question',
            text='Text',
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            heading='Answer',
            text='Text'
        )
        self.update_data = {
            'heading': 'Updated Answer',
            'text': 'Updated text',
        }

        self.url = reverse('answers:answer_detail', kwargs={'id': self.answer.id}) # type: ignore

    def test_get_answer_detail(self):
        response = self.client.get(self.url)
        serializer = AnswerDetailSerializer(self.answer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data) # type: ignore

    def test_put_answer_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.put(self.url, self.update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('heading'), self.update_data['heading']) # type: ignore
        self.assertEqual(response.data.get('text'), self.update_data['text']) # type: ignore
        self.assertEqual(response.data.get('username'), self.user.username) # type: ignore

    def test_delete_question_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Answer.objects.filter(id=self.answer.id).exists()) # type: ignore

    def test_put_question_detail_as_other_user(self):
        self.client.force_login(user=self.other_user)
        response = self.client.put(self.url, self.update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# answer comment create test
class AnswerCommentCreateViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('answers:comment_create')

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.question = Question.objects.create(
            heading='Question',
            text='Text'
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            heading='Answer',
            text='Text'
        )
        self.create_data = {
            "answer": self.answer.id, # type: ignore
            "text": "Comment"
        }
    
    def test_create_comment(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, self.create_data)
        comment = AnswerComment.objects.last()
        serializer = AnswerCommentCreateSerializer(comment)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data) # type: ignore
        self.assertEqual(comment.user, self.user) # type: ignore

    def test_create_comment_unauthenticated(self):
        response = self.client.post(self.url, self.create_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(AnswerComment.objects.exists())

# answer comment detail test
class AnswerCommentDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.other_user = get_user_model().objects.create(
            username='otheruser', email='other@example.com', password='otherpass'
        )
        self.question = Question.objects.create(
            heading='Question',
            text='Text',
        )
        self.answer = Answer.objects.create(
            question=self.question,
            heading='Answer',
            text='Text',
        )
        self.comment = AnswerComment.objects.create(
            text='Comment',
            user=self.user,
            answer=self.answer
        )

        self.url = reverse('answers:comment_detail', kwargs={'id': self.comment.id}) # type: ignore
        self.update_data = {'text': 'Updated comment'}
    
    def test_get_comment_detail(self):
        response = self.client.get(self.url)
        serializer = AnswerCommentDetailSerializer(instance=self.comment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data) # type: ignore

    def test_put_comment_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.put(self.url, self.update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('text'), self.update_data['text']) # type: ignore
    
    def test_delete_comment_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AnswerComment.objects.filter(id=self.comment.id).exists()) # type: ignore

    def test_put_comment_detail_as_other_user(self):
        self.client.force_login(user=self.other_user)
        response = self.client.put(self.url, self.update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# answer set solution test
class AnswerSetSolutionViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('answers:answer_set_solution')

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
        self.answer = Answer.objects.create(
            question=self.question,
            heading='Answer',
            text='Text',
        )

    def test_answer_set_solution(self):
        self.client.force_login(user=self.user)
        
        response = self.client.post(self.url, {'answer': self.answer.id}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('is_solution'))
        self.assertEqual(response.data.get('is_solution'), Answer.objects.get(id=self.answer.id).is_solution)

        response = self.client.post(self.url, {'answer': self.answer.id}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('is_solution'))
        self.assertEqual(response.data.get('is_solution'), Answer.objects.get(id=self.answer.id).is_solution)

    def test_answer_set_solution_invalid_answer(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, {'answer': 999})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_answer_set_solution_as_other_user(self):
        self.client.force_login(user=self.other_user)
        response = self.client.post(self.url, {'answer': self.answer.id}) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# answer rate list test
class AnswerRateListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('answers:rate_list')

    def test_answer_rate_list(self):
        response = self.client.get(self.url) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, AnswerRate.RATE_CHOICES)

# user answer rate test
class UserAnswerRateViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('answers:rate_user')

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.question = Question.objects.create(
            user=self.user,
            heading='Question',
            text='Text',
        )
        self.answer = Answer.objects.create(
            question=self.question,
            heading='Answer',
            text='Text',
        )
        self.answer_rate = AnswerRate.objects.create(
            user=self.user,
            rate=AnswerRate.RATE_RELEVANT,
            answer=self.answer,
        )

    def test_user_answer_rate(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'answer_id': self.answer.id}) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('rate'), self.answer_rate.rate)

    def test_user_answer_rate_unauthenticated(self):
        response = self.client.get(self.url, {'answer_id': self.answer.id}) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# user answer rate test
class AnswerRateCreateViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('answers:rate_create')

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.question = Question.objects.create(
            user=self.user,
            heading='Question',
            text='Text',
        )
        self.answer = Answer.objects.create(
            question=self.question,
            heading='Answer',
            text='Text',
        )

        self.create_data = {
            'answer': self.answer.id,
            'rate': AnswerRate.RATE_RELEVANT
        }
        self.update_data = {
            'answer': self.answer.id,
            'rate': AnswerRate.RATE_USEFUL
        }
        self.delete_data = {
            'answer': self.answer.id
        }

    def test_answer_rate_create_update(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, self.create_data) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.answer_rates.filter(answer=self.answer).exists())

        response = self.client.post(self.url, self.update_data) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.user.answer_rates.filter(answer=self.answer)), 1)

    def test_answer_rate_delete(self):
        self.client.force_login(user=self.user)
        self.client.post(self.url, self.create_data) # type: ignore
        response = self.client.delete(self.url, self.delete_data) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user.answer_rates.filter(answer=self.answer).exists())

