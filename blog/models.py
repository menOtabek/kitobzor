from django.db import models
from abstract_model.base_model import BaseModel

class Post(BaseModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    title = models.CharField(max_length=777)
    like = models.ManyToManyField('authentication.User', related_name='post_likes', blank=True)
    view_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title


class PostComment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    comment = models.TextField()
    like = models.ManyToManyField('authentication.User', related_name='post_comment_likes', blank=True)

    def __str__(self):
        return f'Comment to {self.post} by {self.user}'
