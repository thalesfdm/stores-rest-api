import json

from tests.base_test import BaseTest
from models.store import StoreModel
from models.item import ItemModel

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')

                self.assertEqual(400, response.status_code)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.delete('/store/test')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('/store/test')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')

                self.assertEqual(404, response.status_code)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()
                response = client.get('/store/test')

                self.assertDictEqual({'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 1.99}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('/stores')

                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': []}]},
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()
                response = client.get('/stores')

                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': [
                    {'name': 'test', 'price': 1.99}
                ]}]}, json.loads(response.data))