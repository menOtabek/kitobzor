from django.core.exceptions import ValidationError
from django.db import models
from abstract_model.base_model import BaseModel

COVER_TYPE = (
    (1, 'Hard'),
    (2, 'Soft'),
)

BOOK_STATUS = (
    (1, 'Active'),
    (2, 'Inactive'),
)


class Book(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=150)
    cover_type = models.IntegerField(choices=COVER_TYPE)
    price = models.PositiveIntegerField()
    pages = models.PositiveIntegerField()
    published_at = models.PositiveIntegerField()
    status = models.IntegerField(choices=BOOK_STATUS, default=1)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    book_land = models.BooleanField(default=False)
    like = models.ManyToManyField(to='authentication.User', related_name='book_likes', blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.user and self.user.role not in [1, 2]:
            raise ValidationError('Permission denied')
        self.owner = True
        self.save()


class BookPicture(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    picture = models.ImageField()

    def __str__(self):
        return f'Picture for {self.book.name}'


class BookComment(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    like = models.ManyToManyField(to='authentication.User', blank=True, related_name='book_comment_likes')

    def __str__(self):
        return f'Comment to {self.book.name}'
