from django.db import models
from base.models import District
from abstract_model.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, BaseModel):
    class UserRoles(models.TextChoices):
        SUPERADMIN = 'superadmin', _('superadmin')
        ADMIN = 'admin', _('admin')
        SIMPLE = 'simple', _('simple')
        BOOKSHOP = 'bookshop', _('bookshop')
        LIBRARY = 'library', _('library')

    class Languages(models.TextChoices):
        UZBEK = 'uzbek', _('uzbek')
        ENGLISH = 'english', _('english')
        RUSSIAN = 'russian', _('russian')

    email = None
    EMAIL_FIELD = None
    username = None
    USERNAME_FIELD = None

    bio = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    phone_is_visible = models.BooleanField(default=False)
    location_is_visible = models.BooleanField(default=False)
    telegram_id = models.CharField(max_length=77, unique=True)
    language = models.CharField(max_length=20, choices=Languages.choices, default=Languages.UZBEK)
    role = models.CharField(max_length=20, choices=UserRoles.choices, verbose_name=_('role'), default=UserRoles.SIMPLE)
    is_active = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='users/pictures/', default='users/pictures/default_user.png')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('base.Location', on_delete=models.SET_NULL, null=True, blank=True)

    REQUIRED_FIELDS = ["telegram_id"]

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Otp(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_user')
    otp_code = models.CharField(max_length=6, null=True, blank=True)
