from rest_framework import serializers
from .models import Post, PostComment

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'book_name', 'book_author', 'title')


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ('user', 'post', 'comment')


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'book_name', 'book_author', 'title', 'like')
        extra_kwargs = {
            'user': {'read_only': True},
            'book_name': {'required': False},
            'book_author': {'required': False},
            'title': {'required': False},
            'like': {'required': False},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PostCommentListSerializer(serializers.ModelSerializer):
    comment_like_count = serializers.SerializerMethodField(source='comment_like_count', read_only=True)
    class Meta:
        model = PostComment
        fields = ('user', 'post', 'comment', 'like', 'comment_like_count')


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(source='post_comments', many=True, read_only=True)
    like_count = serializers.IntegerField(source='like_count', read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'user', 'book_name', 'book_author', 'title', 'like', 'like_count')
        read_only_fields = ('id', 'user', 'like')

    def get_post_comments(self, obj):
        comments = PostComment.objects.filter(post=obj)
        return PostCommentListSerializer(comments, many=True).data
