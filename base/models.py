from django.db import models
from abstract_model.base_model import BaseModel
from tinymce.models import HTMLField # Todo  ReachTextfield 6
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models as gis_models


class Region(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(gis_models.Model):
    class LocationType(gis_models.TextChoices):
        BOOKSHOP = 'bookshop', _('bookshop')
        LIBRARY = 'library', _('library')
        HOME = 'home', _('home')
        WORKPLACE = 'workplace', _('workplace')

    point = gis_models.PointField(geography=True, srid=4326, blank=True, null=True)
    type = gis_models.CharField(choices=LocationType.choices, default=LocationType.HOME)


class Banner(BaseModel):
    picture = models.ImageField(upload_to="banner/pictures/")
    title = models.CharField(max_length=400, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class FAQ(BaseModel):
    question = models.CharField(max_length=400)
    answer = HTMLField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class PrivacyPolicy(BaseModel):
    class PolicyType(models.TextChoices):
        PUBLIC = 'public', _('public')
        BOOKSHOP = 'bookshop', _('bookshop')
        LIBRARY = 'library', _('library')
    title = models.CharField(max_length=400)
    description = HTMLField()
    type = models.CharField(choices=PolicyType.choices, default=PolicyType.PUBLIC)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
