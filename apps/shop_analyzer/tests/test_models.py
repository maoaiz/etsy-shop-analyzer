import pytest

from unittest import TestCase
# from unittest.mock import patch

from apps.shop_analyzer.models import Shop


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestModels(TestCase):
    pytestmark = pytest.mark.django_db

    def setUp(self):
        self.shop_id = 123
        self.name = "Fake shop"
        self.title = "Fake title"
        self.url = "https://fake.url"
        self.instance = Shop.objects.create(
            shop_id=self.shop_id,
            name=self.name,
            title=self.title,
            url=self.url,
        )

    def test_meaningful_terms(self):
        self.assertIsInstance(self.instance, Shop)
