from budgets.models import Entry
from core.helpers.test import BaseTestCase
from budgets import factories as budgets_factories


class EntryTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_str(self):
        instance: Entry = budgets_factories.EntryFactory.create()
        self.assertEqual(str(instance), f'{instance.updated.strftime("%Y-%m-%d %H:%M:%S")} | {instance.value}')
