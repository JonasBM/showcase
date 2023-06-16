from accounts.models import UserProfile
from core.helpers.model import TimeStampModelMixin
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import HttpRequest
from django.utils.translation import gettext as _


class Wallet(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name=_('user'))
    balance = models.DecimalField(max_digits=11, decimal_places=2, null=True, verbose_name=_('balance'))

    class Meta:
        ordering = ['name', 'id']
        unique_together = [['name', 'user']]
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')

    def publish(self):
        pass

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'

    @property
    def lastest_entry(self) -> 'Entry':
        return self.entries.order_by('updated').last()

    def has_object_permission(self, request: HttpRequest):
        return self.user == request.user

    def update_balance(self, save=True):
        self.balance = self.entries.aggregate(sum=models.Sum('value'))['sum']
        if save:
            self.save()


class Tag(models.Model):

    GENERIC = 'GN'
    CORRECTION = 'CO'
    BANK = 'BK'
    CARD = 'CD'
    TYPE_CHOICES = [
        (GENERIC, _('generic')),
        (CORRECTION, _('correction')),
        (BANK, _('bank')),
        (CARD, _('card')),
    ]

    name = models.CharField(max_length=100, verbose_name=_('name'))
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name=_('user'))
    type = models.CharField(max_length=2, default=GENERIC, verbose_name=_('type'), choices=TYPE_CHOICES)

    class Meta:
        ordering = ['name', 'id']
        unique_together = [['name', 'user']]
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self) -> str:
        return f'{self.name}'

    def has_object_permission(self, request: HttpRequest):
        return self.user == request.user


class Entry(TimeStampModelMixin, models.Model):

    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='entries', verbose_name=_('wallet'))
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)
    value = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('valor'))
    observation = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('observation'))

    class Meta:
        ordering = ['updated', 'id']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __str__(self) -> str:
        return f'{self.updated.strftime("%Y-%m-%d %H:%M:%S")} | {self.value}'

    @property
    def tags_display(self):
        return ', '.join(tag.name.upper() for tag in self.tags.all())

    def has_object_permission(self, request: HttpRequest):
        return self.wallet.user == request.user


@receiver(post_save, sender=Entry)
def handler_entry_post_save(instance: Entry, **kwargs):
    instance.wallet.update_balance()


@receiver(post_delete, sender=Entry)
def handler_entry_post_delete(instance: Entry, **kwargs):
    instance.wallet.update_balance()
