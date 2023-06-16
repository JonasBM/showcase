import factory
from core.helpers.factory import DjangoModelFactoryWithDictBuild
from django.contrib.auth.hashers import make_password
from . import models

from django.contrib.auth.models import Group


class GroupFactory(DjangoModelFactoryWithDictBuild):
    '''This factory can bring errors, because name is unique'''

    class Meta:
        model = Group

    class Params:
        fake_name = factory.Faker('words', nb=2)

    name = factory.LazyAttributeSequence(lambda o, n: f'{o.fake_name} {n}')


class UserProfileFactory(DjangoModelFactoryWithDictBuild):

    class Meta:
        model = models.UserProfile

    class Params:
        fake_email = factory.Faker('email')
        fake_password = factory.Faker('password')

    email = factory.LazyAttributeSequence(
        lambda o, n: f'{o.fake_email[:o.fake_email.index("@")]}{n}{o.fake_email[o.fake_email.index("@"):]}'
    )
    password = factory.LazyAttribute(lambda o: make_password(o.fake_password))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if extracted and create:
            self.groups.set(extracted)
