from typing import List

from budgets import factories as budgets_factories
from budgets.models import Entry, Tag, Wallet
from core.helpers.test import BaseTestCase


class FactoriesTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_wallet(self):
        entries: List[Entry] = budgets_factories.EntryFactory.create_batch(2)
        instance: Wallet = budgets_factories.WalletFactory.create(entries=entries)
        self.assertGreater(instance.pk, 0)
        instance: Wallet = budgets_factories.WalletFactory.create(entries=2)
        self.assertGreater(instance.pk, 0)

    def test_tag(self):
        instance: Tag = budgets_factories.TagFactory.create()
        self.assertGreater(instance.pk, 0)

    def test_entry(self):
        tags: List[Tag] = budgets_factories.TagFactory.create_batch(2)
        instance: Entry = budgets_factories.EntryFactory.create(tags=tags)
        self.assertGreater(instance.pk, 0)
