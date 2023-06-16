from budgets.models import Tag
from core.helpers.test import BaseTestCase
from budgets import factories as budgets_factories


class TagTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_str(self):
        instance: Tag = budgets_factories.TagFactory.create()
        self.assertEqual(str(instance), instance.name)
