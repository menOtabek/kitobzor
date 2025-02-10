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

RATING_CHOICES = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
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
    isbn = models.CharField(max_length=20)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f'Comment to {self.book.name}'


class BookRating(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)

    def __str__(self):
        return f'Rating: {self.rating}'


class BookCommentRating(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.ForeignKey(BookComment, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)

    def __str__(self):
        return f'Rating for comment of {self.book.name}'


class DefaultBookOffer(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    book_name = models.CharField(max_length=150)
    book_author = models.CharField(max_length=150)

    def __str__(self):
        return f'Offer for {self.book_name}'
