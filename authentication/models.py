from django.db import models
from django.utils.timezone import now

from base.models import District, Region
from abstract_model.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .utils import validate_phone_number


class User(AbstractUser):
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

    email = models.EmailField(unique=True, blank=False, null=False, verbose_name=_('email'))
    username = models.CharField(unique=True, max_length=150, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    last_login = models.DateTimeField(null=True, blank=True, verbose_name=_("last login"))
    is_superuser = models.BooleanField(default=False, verbose_name=_('is superuser'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))
    date_joined = models.DateTimeField(default=now, verbose_name=_("date joined"))

    bio = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('bio'))
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name=_('phone number'))
    app_phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True,
                                        verbose_name=_('phone number'), validators=[validate_phone_number])
    telegram_id = models.CharField(max_length=77, unique=True, verbose_name=_('telegram id'))
    language = models.CharField(max_length=20, choices=Languages.choices, default=Languages.UZBEK,
                                verbose_name=_('language'))
    role = models.CharField(max_length=20, choices=UserRoles.choices, verbose_name=_('role'), default=UserRoles.SIMPLE)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    picture = models.ImageField(upload_to='users/pictures/', default='users/pictures/default_user.png',
                                verbose_name=_('picture'))
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('last name'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('district'))
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('region'))
    location = models.ForeignKey('base.Location', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_('location'))
    location_text = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('location text'))

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = None

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Otp(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_user')
    otp_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f'User: {self.user}'
