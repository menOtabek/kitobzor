from django.db import models
from abstract_model.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class Book(BaseModel):
    class OwnerType(models.TextChoices):
        USER = 'user', _('shop')
        SHOP = 'shop', _('shop')

    class CoverType(models.TextChoices):
        HARD = 'hard', (_('hard'))
        SOFT = 'soft', (_('soft'))


    posted_by = models.ForeignKey(to='authentication.User', on_delete=models.SET_NULL, null=True, related_name='book_user',
                             verbose_name=_('user'))
    shop = models.ForeignKey(to='shop.Shop', on_delete=models.CASCADE, blank=True, null=True, related_name='book_shop')
    picture = models.ImageField(upload_to='books/pictures/', verbose_name=_('picture'))
    owner_type = models.CharField(max_length=4, choices=OwnerType.choices, default=OwnerType.USER, verbose_name=_('owner type'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    language = models.CharField(max_length=55, verbose_name=_('language'))
    script_type = models.CharField(max_length=30, verbose_name=_('script type'), blank=True, null=True)
    description = CKEditor5Field(blank=True, null=True, verbose_name=_('description'))
    author = models.CharField(max_length=255, verbose_name=_('author'))
    cover_type = models.CharField(max_length=4, choices=CoverType.choices, verbose_name=_('cover type'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))
    pages = models.PositiveIntegerField(verbose_name=_('pages number'))
    publication_year = models.PositiveIntegerField(verbose_name=_('publication year'))
    isbn = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('isbn'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_banned = models.BooleanField(default=False, verbose_name=_('is banned'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class BookView(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='book_view_user')
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='book_views_count')

    def __str__(self):
        return f'{self.book}, {self.user}'

    class Meta:
        verbose_name = 'BookView'
        verbose_name_plural = 'BookViews'


class BookLike(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='book_like_user',
                             verbose_name=_('user'))
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='book_likes_count',
                             verbose_name=_('book'))
    type = models.ForeignKey(to='base.LikeCategory', on_delete=models.CASCADE, related_name='book_like_type',
                                  verbose_name=_('type'))

    def __str__(self):
        return f'{self.book.name}, {self.user}'

    class Meta:
        verbose_name = 'BookLike'
        verbose_name_plural = 'BookLikes'


class BookComment(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='book_comment_user',
                             verbose_name=_('user'))
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='book_comments', verbose_name=_('book'))
    comment = models.CharField(max_length=777, verbose_name=_('comment'))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment to {self.book}'

    class Meta:
        verbose_name = 'BookComment'
        verbose_name_plural = 'BookComments'


class BookCommentLike(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, verbose_name=_('user'))
    comment = models.ForeignKey(to='BookComment', on_delete=models.CASCADE, related_name='book_comment_likes',
                                verbose_name=_('comment'))
    type = models.ForeignKey(to='base.LikeCategory', on_delete=models.CASCADE, related_name='book_comment_likes',
                                  verbose_name=_('type'))

    def __str__(self):
        return f'{self.comment}, {self.user}'

    class Meta:
        verbose_name = 'BookCommentLike'
        verbose_name_plural = 'BookCommentLikes'
