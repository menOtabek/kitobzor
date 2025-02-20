from django.db import models
from abstract_model.base_model import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Banner(BaseModel):
    picture = models.ImageField(upload_to="banner/pictures/")
    title = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
