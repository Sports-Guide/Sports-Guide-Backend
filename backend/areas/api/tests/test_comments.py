from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from areas.factories import AreaFactory, CommentFactory, UserFactory

User = get_user_model()


class CommentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.another_user = UserFactory()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            nickname='admin',
            password='adminpassword'
        )
        self.area = AreaFactory()
        self.comment = CommentFactory(author=self.user, area=self.area)
        self.comment_url = reverse('comment-detail', args=[self.comment.id])

    def test_list_comments(self):
        """
        Тест возможности получения списка комментариев.
        """
        response = self.client.get(reverse('comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_comment(self):
        """
        Тест возможности создания нового комментария пользователем.
        """
        self.client.force_authenticate(user=self.user)
        data = {'area': self.area.id, 'comment': 'New Comment'}
        response = self.client.post(reverse('comment-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment_by_author(self):
        """
        Тест возможности обновления комментария его автором.
        """
        self.client.force_authenticate(user=self.user)
        data = {'area': self.area.id, 'comment': 'Updated Comment'}
        response = self.client.put(self.comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment_by_another_user(self):
        """
        Тест невозможности обновления комментария другим пользователем.
        """
        self.client.force_authenticate(user=self.another_user)
        data = {'comment': 'Updated Comment'}
        response = self.client.put(self.comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_by_author(self):
        """
        Тест возможности удаления комментария его автором.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.comment_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_by_another_user(self):
        """
        Тест невозможности удаления комментария другим пользователем.
        """
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(self.comment_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
