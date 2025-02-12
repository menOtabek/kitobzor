from django.db import models
from abstract_model.base_model import BaseModel
from base.models import Region, District

USER_ROLES = (
    (1, 'SuperAdmin'),
    (2, 'Admin'),
    (3, 'BookShop'),
    (4, 'SimpleUser'),
)

class User(BaseModel):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    telegram_id = models.CharField(max_length=77, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=4)
    is_active = models.BooleanField(default=True)
    login_time = models.DateTimeField(null=True)
    otp_code = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='users/pictures', default='')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'Bot id: {self.telegram_id}, Phone number: {self.phone_number}'

    class Meta:
        ordering = ['-created_at']
