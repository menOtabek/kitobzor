from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.contrib.gis.db import models as gis_models


from base.models import BaseModel
from base.models import Region, District


class Shop(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    bio = models.CharField(max_length=500, verbose_name=_("Shop description"))
    picture = ResizedImageField(size=[800, 800], quality=85, force_format='JPEG', upload_to='shop/pictures',
                                verbose_name=_("picture"))
    owner = models.ForeignKey('authentication.User', on_delete=models.PROTECT,
                              related_name='shops', verbose_name=_('Owner'))
    star = models.PositiveIntegerField(default=0, verbose_name=_('Star'))
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='shops', verbose_name=_('District'))
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='shops', verbose_name=_('Region'))
    point = gis_models.PointField(geography=True, srid=4326, blank=True, null=True)
    location_text = models.TextField(verbose_name=_('Location text'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone number'))
    telegram = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Telegram'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Shop')
        verbose_name_plural = _('Shops')


class ShopStuff(BaseModel):
    shop = models.ForeignKey('Shop', on_delete=models.PROTECT, related_name='stuffs', verbose_name=_('Shop'))
    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='stuffs',
                             verbose_name=_('User'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))

    def __str__(self):
        return f'Shop: {self.shop.name}, Admin: {self.user}'

    class Meta:
        verbose_name = _('Shop stuff')
        verbose_name_plural = _('Shop stuffs')


class ShopFeedback(BaseModel):
    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='User_feedback',
                             verbose_name=_('User'))
    message = models.TextField(verbose_name=_('Message'), blank=True, null=True)
    star = models.PositiveIntegerField(verbose_name=_('Star'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_active = models.BooleanField(default=False, verbose_name=_('Is active'))

    def __str__(self):
        return f'Feedback: {self.message}'

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')


class Order(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', _('pending')
        CONFIRMED = 'confirmed', _('confirmed')
        REJECTED = 'rejected', _('rejected')
        SOLD = 'sold', _('sold')

    user = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='user_order',
                             verbose_name=_('User'))
    shop = models.ForeignKey('Shop', on_delete=models.SET_NULL, null=True, related_name='shop_order',
                             verbose_name=_('Shop'))
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name=_('Status'))

    def __str__(self):
        return f'Order: {self.user}'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    book = models.ForeignKey(to='sharing.Book', on_delete=models.SET_NULL, null=True, related_name='book_order',
                             verbose_name=_('Book'))

    @property
    def total_price(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.book.name}"

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
