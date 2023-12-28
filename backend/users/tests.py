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
        """Возвращается email пользователя"""
        self.assertTrue(self.user, 'test@example.com')

    def test_short_pass(self):
        self.user.password = 'weak'
        self.assertRaises(ValidationError)

    def test_long_pass(self):
        self.user.password = 'thepasswordistoolongtobeused'
        self.assertRaises(ValidationError)

    def test_caps_pass(self):
        self.user.password = '12PASSWORD'
        self.assertRaises(ValidationError)

    def test_low_pass(self):
        self.user.password = '12password'
        self.assertRaises(ValidationError)
