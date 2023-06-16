from typing import List

from accounts import factories as accounts_factories
from accounts.models import UserProfile
from core.helpers.test import BaseTestCase
from django.contrib.auth.models import Group


class FactoriesTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_user_profile(self):
        groups: List[Group] = accounts_factories.GroupFactory.create_batch(2)
        instance: UserProfile = accounts_factories.UserProfileFactory.create(groups=groups)
        self.assertGreater(instance.pk, 0)
