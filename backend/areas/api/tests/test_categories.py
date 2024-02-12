from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from areas.factories import CategoryFactory, UserFactory

User = get_user_model()


class CategoryViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            nickname='admin',
            password='adminpassword'
        )
        self.category = CategoryFactory()
        self.category_url = reverse('areas:category-detail',
                                    kwargs={'pk': self.category.pk})

    def test_list_categories(self):
        """
        Тест возможности получения списка категорий.
        """
        response = self.client.get(reverse('areas:category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category_as_admin(self):
        """
        Тест возможности создания категории администратором.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New', 'slug': 'New', 'area_name': 'New area'}
        response = self.client.post(reverse('areas:category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_as_user(self):
        """
        Тест невозможности создания категории обычным пользователем.
        """
        self.client.force_authenticate(user=self.user)
        data = {'name': 'New Category'}
        response = self.client.post(reverse('areas:category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_as_admin(self):
        """
        Тест возможности обновления категории администратором.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New', 'slug': 'New', 'area_name': 'New area'}
        response = self.client.put(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_as_user(self):
        """
        Тест невозможности обновления категории обычным пользователем.
        """
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Category'}
        response = self.client.put(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_as_admin(self):
        """
        Тест возможности удаления категории администратором.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_as_user(self):
        """
        Тест невозможности удаления категории обычным пользователем.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
