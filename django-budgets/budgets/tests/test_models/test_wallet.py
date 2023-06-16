from budgets.models import Wallet, Entry
from core.helpers.test import BaseTestCase
from budgets import factories as budgets_factories


class WalletTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_str(self):
        instance: Wallet = budgets_factories.WalletFactory.create()
        self.assertEqual(str(instance), f'{instance.pk} - {instance.name}')

    def test_lastest_entry(self):
        instance: Wallet = budgets_factories.WalletFactory.create(entries=3)
        self.assertEqual(instance.lastest_entry, Entry.objects.filter(wallet=instance).order_by('updated').last())
