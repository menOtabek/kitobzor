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

class DefaultBookOffer(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    book_name = models.CharField(max_length=150)
    book_author = models.CharField(max_length=150)

    def __str__(self):
        return f'Offer for {self.book_name}'
