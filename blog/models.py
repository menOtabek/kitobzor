from django.db import models
from abstract_model.base_model import BaseModel
from tinymce.models import HTMLField


class Post(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='post_user')
    book_name = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    book_author = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=250, db_index=True)
    description = HTMLField(blank=True, null=True)
    like = models.ManyToManyField(to='authentication.User', related_name='post_likes', blank=True)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    views = models.ManyToManyField(to='authentication.User', related_name='post_views_count', blank=True)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.like.count()

    @property
    def comments_count(self):
        return self.post_comments.count()

    @property
    def views_count(self):
        return self.views.count()


class PostComment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='post_comment_user')
    comment = models.TextField()
    like = models.ManyToManyField(to='authentication.User', related_name='post_comment_likes', blank=True)
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment to {self.post} by {self.user}'

    def comment_like_count(self):
        return self.like.count()

    def replies_count(self):
        return self.replies.count()
