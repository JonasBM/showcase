from django.forms.models import model_to_dict

import factory


class DjangoModelFactoryWithDictBuild(factory.django.DjangoModelFactory):

    @classmethod
    def build_dict(cls, **kwargs):
        """Build an dictionary from the instance of the associated class, with overridden attrs."""
        instance = super().build(**kwargs)
        return model_to_dict(instance)

    @classmethod
    def build_dict_batch(cls, size, **kwargs):
        """Build a batch of dictionaries from the instance of the given class, with overridden attrs.

        Args:
            size (int): the number of instances to build

        Returns:
            object list: the built instances
        """
        list = super().build_batch(size, **kwargs)
        return [model_to_dict(i) for i in list]
