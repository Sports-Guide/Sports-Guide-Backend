from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from areas.constants import ModerationStatus
from areas.factories import (
    AreaFactory,
    CategoryFactory,
    CommentFactory,
    UserFactory,
)

User = get_user_model()


class AreaViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.another_user = UserFactory()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            nickname='admin',
            password='adminpassword'
        )
        self.category = CategoryFactory()
        self.area = AreaFactory(
            author=self.user,
            moderation_status=ModerationStatus.APPROVED.value
        )
        self.another_area = AreaFactory(
            author=self.another_user,
            moderation_status=ModerationStatus.APPROVED.value
        )
        self.area_url = reverse('areas:area-detail', args=[self.area.id])

    def test_list_areas(self):
        """
        Тест возможности получения списка площадок.
        """
        response = self.client.get(reverse('areas:area-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)

    def test_create_area(self):
        """
        Тест возможности создания нового площадки обычным пользователем.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Area',
            'latitude': 11.111111,
            'longitude': 11.111111,
            'categories': [self.category.id],
            'address': 'str',
        }
        response = self.client.post(reverse('areas:area-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_area_by_author(self):
        """
        Тест возможности обновления площадки его автором.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Updated Area',
            'latitude': 11.111111,
            'longitude': 11.111111,
            'categories': [self.category.id],
            'address': 'str',
        }
        response = self.client.put(self.area_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_area_by_another_user(self):
        """
        Тест невозможности обновления площадки другим обычным пользователем.
        """
        self.client.force_authenticate(user=self.another_user)
        data = {'name': 'Updated Area'}
        response = self.client.put(self.area_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_area_by_author(self):
        """
        Тест возможности удаления площадки его автором.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.area_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_area_by_another_user(self):
        """
        Тест невозможности удаления площадки другим обычным пользователем.
        """
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(self.area_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comments(self):
        """
        Тест получения комментариев к конкретной площадке.
        """
        CommentFactory.create_batch(3, area=self.area, author=self.user)
        response = self.client.get(
            reverse('areas:area-detail', args=[self.area.id]) + 'comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_areas_by_user(self):
        """
        Тест получения площадок, созданных пользователем.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('areas:area-my'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
