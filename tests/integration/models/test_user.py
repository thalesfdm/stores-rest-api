from tests.base_test import BaseTest
from models.user import UserModel


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('Test', '123')

            self.assertIsNone(UserModel.find_by_username('Test'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('Test'))
            self.assertIsNotNone(UserModel.find_by_id(1))