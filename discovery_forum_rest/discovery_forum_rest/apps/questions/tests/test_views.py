from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import QuestionCategory, Question, QuestionComment
from questions.serializers import (
    QuestionDetailSerializer, 
    QuestionCreateSerializer, 
    QuestionCommentCreateSerializer, 
    QuestionCommentDetailSerializer
)


# question category list test
class QuestionCategoryListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('questions:category_list')

        self.category1 = QuestionCategory.objects.create(name='Category 1')
        self.category2 = QuestionCategory.objects.create(name='Category 2')

    def test_get_question_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# question list test
class QuestionListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('questions:question_list')

        self.category = QuestionCategory.objects.create(name='Category')
        self.question1 = Question.objects.create(
            heading='Question 1',
            text='Text 1',
            category=self.category
        )
        self.question2 = Question.objects.create(
            heading='Question 2',
            text='Text 2',
            category=self.category
        )

    def test_get_all_questions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_questions_by_category(self):
        response = self.client.get(self.url, {'category_id': self.category.id}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_questions_by_query(self):
        response = self.client.get(self.url, {'q': 'Question 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# user question list test
class UserQuestionListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('questions:question_user_list')

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.category = QuestionCategory.objects.create(name='Category')
        self.question1 = Question.objects.create(
            user=self.user,
            heading='Question 1',
            text='Text 1',
            category=self.category
        )
        self.question2 = Question.objects.create(
            user=self.user,
            heading='Question 2',
            text='Text 2',
            category=self.category
        )

    def test_user_questions_list(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_questions_list_with_username(self):
        response = self.client.get(self.url, {'username': self.user.username}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_questions_list_with_wrong_username(self):
        response = self.client.get(self.url, {'username': 'wrongusername'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_questions_list_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# question comment list test
class QuestionCommentListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('questions:comment_list')

        self.question = Question.objects.create(
            heading="Question",
            text="Text",
        )
        self.comment1 = QuestionComment.objects.create(
            text="Comment 1",
            question=self.question,
        )
        self.comment2 = QuestionComment.objects.create(
            text="Comment 2",
            question=self.question,
        )

    def test_get_comment_list(self):
        response = self.client.get(self.url, {"question_id": self.question.id}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# question create test
class QuestionCreateViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("questions:question_create")

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.category = QuestionCategory.objects.create(name="Category")
        self.create_data = {
            "heading": "Question",
            "text": "Text",
            "category": self.category.id, # type: ignore
        }

    def test_create_question(self):
        self.client.force_login(user=self.user)

        response = self.client.post(self.url, self.create_data)
        question = Question.objects.last()
        serializer = QuestionCreateSerializer(question)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data) # type: ignore
        self.assertEqual(question.user, self.user) # type: ignore

    def test_create_question_unauthenticated(self):
        response = self.client.post(self.url, self.create_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Question.objects.exists())

# question detail test
class QuestionDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.other_user = get_user_model().objects.create(
            username='otheruser', email='other@example.com', password='otherpass'
        )
        self.category = QuestionCategory.objects.create(name="Category")
        self.question = Question.objects.create(
            user=self.user,
            heading='Question',
            text='Text',
        )
        self.update_data = {
            'heading': 'Updated Question',
            'text': 'Updated text',
            'category': self.category.id # type: ignore
        }

        self.url = reverse('questions:question_detail', kwargs={'id': self.question.id}) # type: ignore

    def test_get_question_detail(self):
        response = self.client.get(self.url)
        serializer = QuestionDetailSerializer(self.question)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data) # type: ignore

    def test_put_question_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.put(self.url, self.update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('heading'), self.update_data['heading']) # type: ignore
        self.assertEqual(response.data.get('text'), self.update_data['text']) # type: ignore
        self.assertEqual(response.data.get('category'), self.update_data['category']) # type: ignore
        self.assertEqual(response.data.get('username'), self.user.username) # type: ignore

    def test_delete_question_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(id=self.question.id).exists()) # type: ignore

    def test_put_question_detail_as_other_user(self):
        self.client.force_login(user=self.other_user)
        response = self.client.put(self.url, self.update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# question comment create test
class QuestionCommentCreateViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('questions:comment_create')

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.question = Question.objects.create(
            user=self.user,
            heading='Question',
            text='Text'
        )
        self.create_data = {
            "question": self.question.id, # type: ignore
            "text": "Comment"
        }
    
    def test_create_comment(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, self.create_data)
        comment = QuestionComment.objects.last()
        serializer = QuestionCommentCreateSerializer(comment)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data) # type: ignore
        self.assertEqual(comment.user, self.user) # type: ignore

    def test_create_comment_unauthenticated(self):
        response = self.client.post(self.url, self.create_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(QuestionComment.objects.exists())

# question comment detail test
class QuestionCommentDetailViewTestCase(APITestCase):
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
            user=self.user
        )
        self.comment = QuestionComment.objects.create(
            text='Comment',
            user=self.user,
            question=self.question
        )

        self.url = reverse('questions:comment_detail', kwargs={'id': self.comment.id}) # type: ignore
        self.update_data = {'text': 'Updated comment'}
    
    def test_get_comment_detail(self):
        response = self.client.get(self.url)
        serializer = QuestionCommentDetailSerializer(instance=self.comment)

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
        self.assertFalse(QuestionComment.objects.filter(id=self.comment.id).exists()) # type: ignore

    def test_put_comment_detail_as_other_user(self):
        self.client.force_login(user=self.other_user)
        response = self.client.put(self.url, self.update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# question follow test
class QuestionFollowViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('questions:question_follow')

        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.question1 = Question.objects.create(
            heading='Question 1',
            text='Text 1',
        )
        self.question2 = Question.objects.create(
            user=self.user,
            heading='Question 2',
            text='Text 2',
        )

    def test_question_follow(self):
        self.client.force_login(user=self.user)

        response = self.client.post(self.url, {'question_id': self.question1.id}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.question1.following_users.filter(id=self.user.id).exists()) # type: ignore

        response = self.client.post(self.url, {'question_id': self.question1.id}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.question1.following_users.filter(id=self.user.id).exists()) # type: ignore

    def test_question_follow_invalid_question(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, {'question_id': 999})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_question_follow_by_owner(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, {'question_id': self.question2.id}) # type: ignore

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
