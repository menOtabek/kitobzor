from django.db import models
from abstract_model.base_model import BaseModel
from base.models import Region, District

USER_ROLES = (
    (1, 'SuperAdmin'),
    (2, 'Admin'),
    (3, 'Basic'),
)

class User(BaseModel):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=4)
    bot_id = models.CharField(max_length=77, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=3)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    login_time = models.DateTimeField(null=True)


    def __str__(self):
        return f'Bot id: {self.bot_id} Phone number: {self.phone_number}'

    class Meta:
        ordering = ['-created_at']


class Otp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField()
    request_count = models.IntegerField(default=0)

    def __str__(self):
        return self.otp_code

    class Meta:
        ordering = ['-created_at']


class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        ordering = ['-created_at']
