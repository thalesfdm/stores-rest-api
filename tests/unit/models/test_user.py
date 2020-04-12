from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('Test', '123')

        self.assertEqual('Test', user.username)
        self.assertEqual('123', user.password)