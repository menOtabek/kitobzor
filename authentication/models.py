from django.contrib.gis.db import models
from base.models import Region, District
from django.utils import timezone

USER_ROLES = (
    (1, 'SuperAdmin'),
    (2, 'Admin'),
    (3, 'BookShop'),
    (4, 'SimpleUser'),
)

class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    phone_is_visible = models.BooleanField(default=False)
    location_is_visible = models.BooleanField(default=False)
    telegram_id = models.CharField(max_length=77, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=4)
    is_active = models.BooleanField(default=True)
    login_time = models.DateTimeField(default=timezone.now)
    otp_code = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='users/pictures/', default='users/pictures/default_user.png')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.PointField(geography=True, srid=4326, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Bot id: {self.telegram_id}'

    class Meta:
        ordering = ['-created_at']
