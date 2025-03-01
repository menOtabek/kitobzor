from django.db import models
from abstract_model.base_model import BaseModel
from tinymce.models import HTMLField


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
    title = models.CharField(max_length=400)
    description = HTMLField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
