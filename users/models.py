from django.db import models
from django_resized import ResizedImageField
from django.contrib.gis.db import models as gis_models

from base.models import District, Region
from abstract_model.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .utils import validate_phone_number
from utils.choices import Languages, UserRoles

class User(AbstractUser, BaseModel):

    username = None
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_('email'))
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('bio'))
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name=_('phone number'))
    app_phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True,
                                        verbose_name=_('app phone number'), validators=[validate_phone_number])
    telegram_id = models.CharField(max_length=77, unique=True, verbose_name=_('telegram id'))
    language = models.CharField(max_length=20, choices=Languages.choices, default=Languages.UZBEK,
                                verbose_name=_('language'))
    role = models.CharField(max_length=20, choices=UserRoles.choices, verbose_name=_('role'), default=UserRoles.SIMPLE)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    picture = ResizedImageField(size=[1200, 1200], quality=85, force_format='JPEG', upload_to='users/pictures/',
                                default='users/pictures/default_user.png', verbose_name=_('picture'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('district'))
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('region'))
    point = gis_models.PointField(geography=True, srid=4326, blank=True, null=True)
    location_text = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('location text'))

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone_number'

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
