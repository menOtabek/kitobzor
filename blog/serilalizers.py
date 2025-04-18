from rest_framework import serializers
from .models import Post, PostComment
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from authentication.models import User
import html2text


class PostParamValidateSerializer(serializers.Serializer):
    page_number = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    is_popular = serializers.BooleanField(required=False, default=False)
    q = serializers.CharField(required=False, default='')

    def validate(self, attrs):
        if attrs.get('page_number') < 1 or attrs.get('page_size') < 1:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Page and page size must be positive integer')
        return attrs


class PostCreateSwaggerRequestSerializer(serializers.Serializer):
    book_name = serializers.CharField(required=False)
    book_author = serializers.CharField(required=False)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'book_name', 'book_author', 'title', 'description')


class PostCommentSwaggerRequestSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)
    parent = serializers.IntegerField(required=False)


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ('user', 'post', 'comment', 'parent')
        extra_kwargs = {
            'parent': {'required': False},
        }

    def validate(self, attrs):
        if attrs.get('parent'):
            post_comment = PostComment.objects.filter(pk=attrs['parent'].id).first()
            if attrs['post'].id != post_comment.post.id:
                raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Post id and comment id do not match')
            return attrs
        return attrs


class PostUpdateSwaggerRequestSerializer(serializers.Serializer):
    book_name = serializers.CharField(required=False)
    book_author = serializers.CharField(required=False)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'book_name', 'book_author', 'title', 'is_active', 'description')


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'picture')


class PostCommentListSerializer(serializers.ModelSerializer):
    replies_count = serializers.IntegerField(read_only=True)
    comment_like_count = serializers.IntegerField(read_only=True)
    is_comment_liked = serializers.SerializerMethodField()
    user = UserPostSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'post', 'comment', 'comment_like_count', 'is_comment_liked', 'parent', 'replies_count',
                  'created_at', 'user')

    def get_is_comment_liked(self, obj):
        user = self.context.get('request').user if 'request' in self.context else None
        if user and obj.like.filter(id=user.id).exists():
            return True
        return False


class PostListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    user = UserPostSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
        'id', 'book_name', 'book_author', 'title', 'is_liked', 'like_count',
        'comments_count', 'views_count', 'created_at', 'updated_at', 'user')
        read_only_fields = ('id', 'user')

    def get_is_liked(self, obj):
        user = self.context.get('request').user if 'request' in self.context else None
        if user and obj.like.filter(id=user.id).exists():
            return True
        return False


class PostDetailSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    comments = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    user = UserPostSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'book_name', 'book_author', 'title', 'is_liked', 'is_active', 'like_count', 'is_owner',
                  'comments_count', 'views_count', 'created_at', 'updated_at', 'description', 'user', 'comments')
        read_only_fields = ('id', 'user')

    def get_description(self, obj):
        if obj.description:
            return html2text.html2text(obj.description)
        return ""

    def get_comments(self, obj):
        comments = PostComment.objects.filter(post=obj, is_banned=False)
        return PostCommentListSerializer(comments, many=True, context=self.context).data

    def get_is_liked(self, obj):
        user = self.context.get('request').user if 'request' in self.context else None
        if user and obj.like.filter(id=user.id).exists():
            return True
        return False

    def get_is_owner(self, obj):
        user = self.context.get('request').user if 'request' in self.context else None
        if user and obj.user.id == user.id:
            return True
        return False
