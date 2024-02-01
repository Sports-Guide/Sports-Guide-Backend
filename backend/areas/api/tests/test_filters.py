from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from areas.constants import ModerationStatus
from areas.factories import AreaFactory, CategoryFactory, UserFactory

User = get_user_model()


class AreaFilterTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category1 = CategoryFactory()
        self.category2 = CategoryFactory()
        self.area1 = AreaFactory(
            author=self.user,
            moderation_status=ModerationStatus.APPROVED.value
        )
        self.area1.categories.set([self.category1])
        self.area2 = AreaFactory(
            author=self.user,
            moderation_status=ModerationStatus.APPROVED.value
        )
        self.area2.categories.set([self.category1, self.category2])
        self.area3 = AreaFactory(
            author=self.user,
            moderation_status=ModerationStatus.APPROVED.value
        )
        self.area3.categories.set([self.category2])

    def test_filter_by_category(self):
        url = reverse('areas:area-list')
        response = self.client.get(url, {'categories': self.category1.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.area1.id)
        self.assertEqual(response.data[1]['id'], self.area2.id)

    def test_filter_by_nonexistent_category(self):
        url = reverse('areas:area-list')
        response = self.client.get(url, {'categories': 'nonexistent-category'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_multiple_categories(self):
        url = reverse('areas:area-list')
        response = self.client.get(
            url,
            {'categories': [self.category1.slug, self.category2.slug]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[1]['id'], self.area2.id)
        self.assertEqual(response.data[0]['id'], self.area1.id)
