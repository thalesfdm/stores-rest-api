from tests.unit.unit_base_test import UnitBaseTest
from models.item import ItemModel


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('Test', 1.99, 1)

        self.assertEqual('Test', item.name)
        self.assertEqual(1.99, item.price)
        self.assertEqual(1, item.store_id)
        self.assertIsNone(item.store)

    def test_item_json(self):
        item = ItemModel('Test', 1.99, 1)
        expected = {'name': 'Test', 'price': 1.99}

        self.assertEqual(expected, item.json())
