from django.db import models
from abstract_model.base_model import BaseModel
from django_ckeditor_5.fields import CKEditor5Field

class Post(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='post_user')
    book_name = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    book_author = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=250, db_index=True)
    description = CKEditor5Field(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.post_likes.count()

    @property
    def comments_count(self):
        return self.post_comment_user.count()

    @property
    def views_count(self):
        return self.post_views.count()


class PostLike(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(to='blog.Post', on_delete=models.CASCADE, related_name='post_likes')
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return f'Like to {self.post} by {self.user}'


class PostView(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='post_views')
    post = models.ForeignKey(to='blog.Post', on_delete=models.CASCADE, related_name='post_views')

    def __str__(self):
        return f'{self.post} viewed by {self.user}'


class PostComment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='post_comment_user')
    comment = models.TextField()
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment to {self.post} by {self.user}'

    def comment_like_count(self):
        return self.post_comment_likes.count()

    def replies_count(self):
        return self.replies.count()


class PostCommentLike(BaseModel):
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE, related_name='post_comment_likes')
    post_comment = models.ForeignKey(to='blog.PostComment', on_delete=models.CASCADE, related_name='post_comment_likes')

    def __str__(self):
        return f'Like to {self.post_comment} by {self.user}'
