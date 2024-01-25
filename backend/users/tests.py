import os

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CustomUserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            nickname='testnick',
            password='testpass123'
        )

    def tearDown(self):
        for user in User.objects.all():
            if user.photo and os.path.isfile(user.photo.path):
                os.remove(user.photo.path)
            user.delete()

    def test_user_registration(self):
        """
        Тестирование регистрации пользователя.
        """
        url = reverse('customuser-list')
        data = {
            'email': 'user@example.com',
            'nickname': 'nickname',
            'password': 'Nfekso2W'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """
        Тестирование входа в систему и получения токена.
        """
        url = reverse('jwt-create')
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_token_refresh(self):
        """
        Тестирование обновления токена.
        """
        url = reverse('jwt-create')
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        refresh_token = response.data['refresh']

        url = reverse('jwt-refresh')
        data = {'refresh': refresh_token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_password_with_no_lower_case(self):
        """
        Тест валидации пароля без символов в нижнем регистре через API.
        """
        url = reverse('customuser-list')
        data = {
            'email': 'user@example.com',
            'nickname': 'usernick',
            'password': 'PASSWORD123!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_with_no_upper_case(self):
        """
        Тест валидации пароля без символов в верхнем регистре через API.
        """
        url = reverse('customuser-list')
        data = {
            'email': 'user@example.com',
            'nickname': 'usernick',
            'password': 'password123!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_with_non_latin_characters(self):
        """
        Тест валидации пароля с не латинскими символами через API.
        """
        url = reverse('customuser-list')
        data = {
            'email': 'user@example.com',
            'nickname': 'usernick',
            'password': 'Passwørd123!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_password(self):
        """
        Тест валидации корректного пароля через API.
        """
        url = reverse('customuser-list')
        data = {
            'email': 'user@example.com',
            'nickname': 'usernick',
            'password': 'ValidPassword123!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
