from tests.base_test import BaseTest
from models.store import StoreModel
from models.item import ItemModel

class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('Test')

        self.assertListEqual([], store.items.all())

    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test')

            self.assertIsNone(StoreModel.find_by_name('Test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('Test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('Test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test Store')
            item = ItemModel('Test Item', 1.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(1, store.items.count())
            self.assertEqual('Test Item', store.items.first().name)

    def test_store_json(self):
        store = StoreModel('Test')
        expected = {'name': 'Test', 'items': []}

        self.assertDictEqual(expected, store.json())

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('Test Store')
            item = ItemModel('Test Item', 1.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {'name': 'Test Store', 'items': [
                {'name': 'Test Item', 'price': 1.99}
            ]}

            self.assertDictEqual(expected, store.json())