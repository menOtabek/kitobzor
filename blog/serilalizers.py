from rest_framework import serializers
from .models import Post, PostComment
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes

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
        if 'parent' in attrs:
            post_comment = PostComment.objects.filter(pk=attrs['parent'].id).first()
            if attrs['post'].id != post_comment.post.id:
                raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Post id and parent id do not match')
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
        extra_kwargs = {
            'user': {'required': True},
            'book_name': {'required': False},
            'book_author': {'required': False},
            'title': {'required': False},
            'is_active': {'required': False},
            'description': {'required': False}
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PostCommentListSerializer(serializers.ModelSerializer):
    replies_count = serializers.IntegerField(read_only=True)
    comment_like_count = serializers.IntegerField(read_only=True)
    is_comment_liked = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ('id', 'user', 'post', 'comment', 'comment_like_count', 'is_comment_liked', 'parent', 'replies_count')

    def get_is_comment_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False


class PostListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'book_name', 'book_author', 'title', 'is_liked', 'like_count', 'comments_count')
        read_only_fields = ('id', 'user')

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False


class PostDetailSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    comments = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'book_name', 'book_author', 'title', 'is_liked',
                  'like_count', 'is_active', 'comments', 'description', 'comments_count')
        read_only_fields = ('id', 'user')

    def get_comments(self, obj):
        comments = PostComment.objects.filter(post=obj, is_banned=False)
        return PostCommentListSerializer(comments, many=True, context=self.context).data

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False
