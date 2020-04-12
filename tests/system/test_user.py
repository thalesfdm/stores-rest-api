from tests.base_test import BaseTest
from models.user import UserModel
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                data = {'username': 'Test', 'password': '123'}
                response = client.post('/register', data=data)

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(UserModel.find_by_username('Test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                data = {'username': 'Test', 'password': '123'}
                client.post('/register', data=data)
                response = client.post('/auth',
                                       data=json.dumps(data),
                                       headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                data = {'username': 'Test', 'password': '123'}
                client.post('/register', data=data)
                response = client.post('/register', data=data)

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': 'An user with that username already exists'},
                                     json.loads(response.data))
