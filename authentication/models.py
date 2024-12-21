from django.db import models
from abstract_model.base_model import BaseModel
from base.models import Region, District

USER_STATUS_CHOICES = (
    (1, 'Active'),
    (2, 'Inactive'),
)

USER_ROLES = (
    (1, 'Basic'),
    (2, 'ShopManager')
)

class User(BaseModel):
    first_name = models.CharField(max_length=77, default="Unknown")
    last_name = models.CharField(max_length=77, default="User")
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=6)
    bot_id = models.CharField(max_length=77, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=1)
    status = models.IntegerField(choices=USER_STATUS_CHOICES, default=1)
    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    login_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
