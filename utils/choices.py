from django.db import models
from django.utils.translation import gettext_lazy as _



class UserRoles(models.TextChoices):
    SUPERADMIN = 'superadmin', _('superadmin')
    ADMIN = 'admin', _('admin')
    SIMPLE = 'simple', _('simple')
    PREMIUM = 'premium', _('premium')
    PUBLISHER = 'publisher', _('publisher')
    LIBRARY = 'library', _('library')


class Languages(models.TextChoices):
    UZBEK = 'uzbek', _('uzbek')
    ENGLISH = 'english', _('english')
    RUSSIAN = 'russian', _('russian')


class PolicyType(models.TextChoices):
    PUBLIC = 'public', _('public')
    BOOKSHOP = 'bookshop', _('bookshop')
    LIBRARY = 'library', _('library')


class OwnerType(models.TextChoices):
    USER = 'user', _('user')
    SHOP = 'shop', _('shop')

class CoverType(models.TextChoices):
    HARD = 'hard', (_('hard'))
    SOFT = 'soft', (_('soft'))


class BookType(models.TextChoices):
    GIFT = 'gift', _('gift')
    EXCHANGE = 'exchange', _('exchange')
    SELLER = 'seller', _('seller')
