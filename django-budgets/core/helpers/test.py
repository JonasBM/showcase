import logging

import faker
from django.test import TestCase


class BaseTestCase(TestCase):

    def setUp(self):
        '''Create clients for test'''
        logger = logging.getLogger('django.request')
        logger.setLevel(logging.ERROR)

        self.faker = faker.Faker(locale='pt_BR')
