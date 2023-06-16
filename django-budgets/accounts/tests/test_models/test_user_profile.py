from accounts.models import UserProfile
from core.helpers.test import BaseTestCase


class UserProfileTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_str(self):
        email = self.faker.email()
        user = UserProfile(email=email)
        self.assertEqual(str(user), email)

    def test_create_user(self):
        email = self.faker.email()
        password = 'password'
        self.assertRaises(ValueError, UserProfile.objects.create_user, email=None, password=password)
        user = UserProfile.objects.create_user(email=email, password=password)
        self.assertIsNotNone(user)

    def test_create_superuser(self):
        email = self.faker.email()
        self.assertRaises(ValueError, UserProfile.objects.create_superuser, email=None, is_staff=False)
        self.assertRaises(ValueError, UserProfile.objects.create_superuser, email=None, is_superuser=False)
        user = UserProfile.objects.create_superuser(email=email)
        self.assertIsNotNone(user)
