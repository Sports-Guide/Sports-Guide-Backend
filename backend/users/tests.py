from django.forms import ValidationError
from django.test import TestCase
from .models import CustomUser


class UserModelTest(TestCase):
    """
    Тестирование модели пользователя
    """
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            nickname='testuser'
        )

    def test_user_creation(self):
        """Все поля соответсвуют ожидаемым"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.nickname, 'testuser')
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertIsNotNone(self.user.date_joined)

    def test_return_nickname(self):
        """Возвращается ник пользователя"""
        self.assertTrue(self.user, 'testuser')

    def test_password_validation(self):
        with self.assertRaises(ValidationError):
            self.user.password = 'weak'
            self.user.full_clean()

        with self.assertRaises(ValidationError):
            self.user.password = 'thispasswordiswaytoolongandshouldfail'
            self.user.full_clean()

        with self.assertRaises(ValidationError):
            self.user.password = 'alllowercase'
            self.user.full_clean()

        with self.assertRaises(ValidationError):
            self.user.password = 'ALLUPPERCASE'
            self.user.full_clean()

        self.user.password = 'StrongPassword123'
        self.user.full_clean()
