from io import BytesIO
import os

from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class CustomUserTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            nickname='testnick',
            password='testpass123'
        )

    def tearDown(self):
        for user in CustomUser.objects.all():
            if user.photo and os.path.isfile(user.photo.path):
                os.remove(user.photo.path)
            user.delete()

    def test_user_registration(self):
        """
        Тестирование регистрации пользователя.
        """
        url = reverse('users:customuser-list')
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
        url = reverse('users:jwt-create')
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_token_refresh(self):
        """
        Тестирование обновления токена.
        """
        url = reverse('users:jwt-create')
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        refresh_token = response.data['refresh']

        url = reverse('users:jwt-refresh')
        data = {'refresh': refresh_token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_password_with_no_lower_case(self):
        """
        Тест валидации пароля без символов в нижнем регистре через API.
        """
        url = reverse('users:customuser-list')
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
        url = reverse('users:customuser-list')
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
        url = reverse('users:customuser-list')
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
        url = reverse('users:customuser-list')
        data = {
            'email': 'user@example.com',
            'nickname': 'usernick',
            'password': 'ValidPassword123!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @staticmethod
    def get_photo():
        """
        Функция генерации фотографии.
        """
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test_photo.png'
        file.seek(0)
        return file

    def test_add_photo_correctly(self):
        """
        Тестирование загрузки фотографии пользователя.

        """
        self.client.force_authenticate(user=self.user)
        self.photo = self.get_photo()
        payload = {
            "photo": self.photo
        }
        response = self.client.post(
            reverse(
                'users:customuser-upload-photo',
            ),
            data=payload,
            format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('photo' in response.data)
        self.assertIsNotNone(response.data['photo'])
        self.user.refresh_from_db(fields=['photo'])
        self.assertTrue(self.user.photo)

    def test_upload_photo_without_photo(self):
        """
        Тест обработки запроса без передачи фото.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(
                'users:customuser-upload-photo',
            ),
            format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"detail": "Фото не найдено."})

    def test_upload_photo_without_authentication(self):
        """
        Тестирование загрузки фотографии без аутентификации пользователя.
        """
        self.photo = self.get_photo()
        payload = {
            "photo": self.photo
        }
        response = self.client.post(
            reverse('users:customuser-upload-photo'),
            data=payload,
            format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
