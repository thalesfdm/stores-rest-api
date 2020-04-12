from tests.base_test import BaseTest
from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '123').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '123'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = 'JWT ' + auth_token

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')

                self.assertEqual(401, response.status_code)


    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test',
                                      headers={'Authorization': self.access_token})

                self.assertEqual(404, response.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()
                response = client.get('/item/test',
                                      headers={'Authorization': self.access_token})

                self.assertEqual(200, response.status_code)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()
                response = client.delete('/item/test')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                data = {'price': 1.99, 'store_id': 1}
                response = client.post('item/test', data=data)

                self.assertEqual(201, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 1.99},
                                     json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()
                data = {'price': 1.99, 'store_id': 1}
                response = client.post('item/test', data=data)

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                data = {'price': 1.99, 'store_id': 1}
                response = client.put('/item/test', data=data)

                self.assertEqual(200, response.status_code)
                self.assertEqual(1.99, ItemModel.find_by_name('test').price)
                self.assertDictEqual({'name': 'test', 'price': 1.99},
                                     json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 2.99, 1).save_to_db()

                self.assertEqual(2.99, ItemModel.find_by_name('test').price)

                data = {'price': 1.99, 'store_id': 1}
                response = client.put('/item/test', data=data)

                self.assertEqual(200, response.status_code)
                self.assertEqual(1.99, ItemModel.find_by_name('test').price)
                self.assertDictEqual({'name': 'test', 'price': 1.99},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 1.99, 1).save_to_db()

                response = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 1.99}]},
                                     json.loads(response.data))