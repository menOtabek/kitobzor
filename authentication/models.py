from uuid import uuid4
from django.db import models
from abstract_model.base_model import BaseModel
from base.models import Region, District

USER_ROLES = (
    (1, 'SuperAdmin'),
    (2, 'Admin'),
    (3, 'Basic'),
)

class User(BaseModel):
    full_name = models.CharField(max_length=100, default="Unknown")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    password = models.CharField(max_length=6)
    bot_id = models.CharField(max_length=77, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=3)
    is_active = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    is_verified = models.BooleanField(default=False)
    login_time = models.DateTimeField(null=True)

    @property
    def is_authenticated(self):
        if User.objects.filter(id=self.pk).exists():
            return True
        return False

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at']


class Otp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField()
    otp_key = models.UUIDField(default=uuid4, editable=False)
    request_count = models.IntegerField(default=0)

    def __str__(self):
        return self.otp_code

    class Meta:
        ordering = ['-created_at']


class Location(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_main = models.BooleanField(default=False)
