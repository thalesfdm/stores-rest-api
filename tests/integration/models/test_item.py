from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('Test').save_to_db()
            item = ItemModel('Test', 1.99, 1)

            self.assertIsNone(ItemModel.find_by_name('Test'))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('Test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('Test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test Store')
            item = ItemModel('Test Item', 1.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual('Test Store', item.store.name)