from django.db import models
from abstract_model.base_model import BaseModel
from tinymce.models import HTMLField

COVER_TYPE = (
    (1, 'Hard'),
    (2, 'Soft'),
)


class Book(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='book_user')
    picture = models.ImageField(upload_to='books/pictures/')
    name = models.CharField(max_length=100)
    description = HTMLField(blank=True, null=True)
    author = models.CharField(max_length=150)
    cover_type = models.IntegerField(choices=COVER_TYPE)
    price = models.PositiveIntegerField()
    pages = models.PositiveIntegerField()
    publication_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=20, blank=True, null=True)
    views = models.ManyToManyField(to='authentication.User', related_name='book_views_count', blank=True)
    like = models.ManyToManyField(to='authentication.User', related_name='book_likes', blank=True)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def views_count(self):
        return self.views.count()

    @property
    def likes_count(self):
        return self.like.count()

    @property
    def comments_count(self):
        return self.book_comments.count()


class BookComment(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='book_comments')
    comment = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    like = models.ManyToManyField(to='authentication.User', blank=True, related_name='book_comment_likes')
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment to {self.book.name}'

    @property
    def likes_count(self):
        return self.like.count()

    @property
    def replies_count(self):
        return self.replies.count()
