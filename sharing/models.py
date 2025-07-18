from django.db import models
from abstract_model.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from utils.choices import OwnerType, CoverType, BookType


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category name'))
    picture = ResizedImageField(upload_to='books/categories', null=True, blank=True, verbose_name=_('category picture'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

class Book(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('category'), related_name='books', null=True)
    posted_by = models.ForeignKey(to='users.User', on_delete=models.SET_NULL, null=True, related_name='book_user',
                             verbose_name=_('user'))
    exchange_book = models.CharField(max_length=100, verbose_name=_('Exchange book'), blank=True, null=True)
    type = models.CharField(verbose_name=_('book type'), max_length=10, choices=BookType.choices)
    shop = models.ForeignKey(to='shop.Shop', on_delete=models.CASCADE, blank=True, null=True, related_name='book_shop')
    picture = ResizedImageField(size=[800, 800], quality=85, force_format='JPEG', upload_to='books/pictures/', verbose_name=_('picture'))
    owner_type = models.CharField(max_length=4, choices=OwnerType.choices, default=OwnerType.USER, verbose_name=_('owner type'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    language = models.CharField(max_length=55, verbose_name=_('language'))
    script_type = models.CharField(max_length=30, verbose_name=_('script type'), blank=True, null=True)
    description = CKEditor5Field(blank=True, null=True, verbose_name=_('description'))
    author = models.CharField(max_length=255, verbose_name=_('author'))
    cover_type = models.CharField(max_length=4, choices=CoverType.choices, verbose_name=_('cover type'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'), blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('discount price'), blank=True, null=True)
    pages = models.PositiveIntegerField(verbose_name=_('pages number'))
    publication_year = models.PositiveIntegerField(verbose_name=_('publication year'))
    isbn = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('isbn'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_banned = models.BooleanField(default=False, verbose_name=_('is banned'))

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.discount_price and self.price:
            discount = self.price - self.discount_price
            return int((discount / self.price) * 100)
        return None

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    @property
    def like_count(self):
        return self.book_likes_count.count()

    @property
    def view_count(self):
        return self.book_view_user.count()

    @property
    def comment_count(self):
        return self.book_comment_user.count()


class BookView(BaseModel):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='book_view_user')
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='book_view_user')

    def __str__(self):
        return f'{self.book}, {self.user}'

    class Meta:
        verbose_name = 'BookView'
        verbose_name_plural = 'BookViews'


class BookLike(BaseModel):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='book_like_user',
                             verbose_name=_('user'))
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='book_likes_count',
                             verbose_name=_('book'))

    def __str__(self):
        return f'{self.book.name}, {self.user}'

    class Meta:
        verbose_name = 'BookLike'
        verbose_name_plural = 'BookLikes'


class BookComment(BaseModel):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='book_comment_user',
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
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name=_('user'))
    comment = models.ForeignKey(to='BookComment', on_delete=models.CASCADE, related_name='book_comment_likes',
                                verbose_name=_('comment'))

    def __str__(self):
        return f'{self.comment}, {self.user}'

    class Meta:
        verbose_name = 'BookCommentLike'
        verbose_name_plural = 'BookCommentLikes'
