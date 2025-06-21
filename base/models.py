from django.db import models
from abstract_model.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models as gis_models
from django_ckeditor_5.fields import CKEditor5Field


class Region(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'


class District(BaseModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'


class Banner(BaseModel):
    picture = models.ImageField(upload_to="banner/pictures/")
    title = models.CharField(max_length=400, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'


class FAQ(BaseModel):
    question = models.CharField(max_length=500, verbose_name=_("FAQ question"))
    answer = CKEditor5Field(verbose_name=_("FAQ answer"))
    is_active = models.BooleanField(default=False, verbose_name=_("Is active?"))

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'


class PrivacyPolicy(BaseModel):
    class PolicyType(models.TextChoices):
        PUBLIC = 'public', _('public')
        BOOKSHOP = 'bookshop', _('bookshop')
        LIBRARY = 'library', _('library')

    title = models.CharField(max_length=400, verbose_name=_("Title"))
    description = CKEditor5Field(verbose_name=_("Description"))
    type = models.CharField(choices=PolicyType.choices, default=PolicyType.PUBLIC, verbose_name=_("Policy"))
    is_active = models.BooleanField(default=False, verbose_name=_("Is active"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'PrivacyPolicy'
        verbose_name_plural = 'PrivacyPolicies'


class BasePost(BaseModel):
    title = models.CharField(max_length=400, verbose_name=_("Title"), blank=True, null=True)
    book_name = models.CharField(max_length=200, verbose_name=_("Book name"), blank=True, null=True)
    book_author = models.CharField(max_length=200, verbose_name=_("Author"), blank=True, null=True)
    description = CKEditor5Field(verbose_name=_("Description"), blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'BasePost'
        verbose_name_plural = 'BasePosts'


class BasePostView(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, verbose_name=_("User"),
                             related_name='views')
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, verbose_name=_("Post"), related_name='views')

    def __str__(self):
        return f'{self.user} - {self.post}'

    class Meta:
        verbose_name = 'BasePostView'
        verbose_name_plural = 'BasePostViews'


class BasePostLike(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, verbose_name=_("User"))
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, verbose_name=_("Base post"))

    def __str__(self):
        return f'{self.user} - {self.post}'

    class Meta:
        verbose_name = 'BasePostLike'
        verbose_name_plural = 'BasePostLikes'


class BasePostComment(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, verbose_name=_("User"),
                             related_name='user_comments')
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, verbose_name=_("Base post"),
                             related_name='base_post_comments')
    comment = models.TextField(verbose_name=_("Comment"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return f'{self.user} - {self.post}'

    class Meta:
        verbose_name = 'BasePostComment'
        verbose_name_plural = 'BasePostComments'


class BasePostCommentLike(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, verbose_name=_("User"))
    comment = models.ForeignKey(BasePostComment, on_delete=models.CASCADE, verbose_name=_("Comment"))

    def __str__(self):
        return f'{self.user} - {self.comment}'

    class Meta:
        verbose_name = 'BasePostCommentLike'
        verbose_name_plural = 'BasePostCommentLikes'
