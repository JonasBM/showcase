import factory
from accounts import factories as accounts_factories
from core.helpers.factory import DjangoModelFactoryWithDictBuild

from budgets import models


class WalletFactory(DjangoModelFactoryWithDictBuild):

    class Meta:
        model = models.Wallet

    name = factory.Faker('words', nb=2)
    user = factory.SubFactory(accounts_factories.UserProfileFactory)

    @factory.post_generation
    def entries(self, create, extracted, **kwargs):
        if extracted and create:
            if isinstance(extracted, int):
                self.entries.set(EntryFactory.create_batch(extracted, **kwargs))
            else:
                self.entries.set(extracted)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if instance.entries:
            # FIXME: implement balance calculation
            instance.balance = 0
            if create:
                instance.save()
        return super()._after_postgeneration(instance, create, results)


class TagFactory(DjangoModelFactoryWithDictBuild):

    class Meta:
        model = models.Tag

    class Params:
        fake_name = factory.Faker('word')

    name = factory.LazyAttributeSequence(lambda o, n: f'{o.fake_name}{n}')
    user = factory.SubFactory(accounts_factories.UserProfileFactory)


class EntryFactory(DjangoModelFactoryWithDictBuild):

    class Meta:
        model = models.Entry

    wallet = factory.SubFactory(WalletFactory)
    value = factory.Faker('pydecimal', left_digits=4, right_digits=2, max_value=9999)
    observation = None

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if extracted:
            self.tags.set(extracted)
            if create:
                self.save()
