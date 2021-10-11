import pytest

from unittest import TestCase
# from unittest.mock import patch

from apps.shop_analyzer.models import Shop, Item


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
        self.items = [
            {'item_id': 21354, 'name': 'The first item', 'description': 'the first title'},
            {'item_id': 23544, 'name': 'Second item', 'description': 'Second item'},
            {'item_id': 23456, 'name': 'Other item name', 'description': 'Other name'},
            {'item_id': 67834, 'name': 'Same item name', 'description': 'Same name'},
            {'item_id': 75466, 'name': 'What is your name', 'description': 'What is your name'},
            {'item_id': 56422, 'name': 'home work', 'description': 'home work'},
            {'item_id': 65456, 'name': 'Simon Data', 'description': 'Simon Data'},
            {'item_id': 75643, 'name': 'Data transfer', 'description': 'Data transfer'},
            {'item_id': 58643, 'name': 'Big data', 'description': 'Big data'},
        ]

        bulk = [Item(shop=self.instance, **q) for q in self.items]

        Item.objects.bulk_create(bulk)

    def test_create_shop(self):
        self.assertIsInstance(self.instance, Shop)

    def test_num_items_related(self):

        num_items = self.instance.get_num_items()

        self.assertEqual(len(self.items), num_items)

    def test_get_meaningful_terms(self):
        data = [{'term': 'item', 'count': 5}, {'term': 'data', 'count': 6}, {'term': 'name', 'count': 6}]

        terms = self.instance.get_meaningful_terms(2)

        self.assertEqual(terms, data)
