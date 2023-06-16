from accounts import factories as accounts_factories
from core.helpers.test import BaseTestCase


class DjangoModelFactoryWithDictBuildTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_build_dict(self):
        email = self.faker.email()
        model_dict = accounts_factories.UserProfileFactory.build_dict(email=email)
        self.assertTrue(isinstance(model_dict, dict))
        self.assertIsNone(model_dict.get('pk'))
        self.assertEqual(model_dict.get('email'), email)

    def test_build_dict_batch(self):
        batch_number = 2
        list_model_dict = accounts_factories.UserProfileFactory.build_dict_batch(batch_number)
        self.assertTrue(isinstance(list_model_dict, list))
        self.assertEqual(len(list_model_dict), batch_number)
        for dict in list_model_dict:
            self.assertIsNone(dict.get('pk'))
