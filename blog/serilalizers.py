from rest_framework import serializers
from .models import Post, PostComment
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class PostCreateSwaggerRequestSerializer(serializers.Serializer):
    book_name = serializers.CharField(required=True)
    book_author = serializers.CharField(required=True)
    title = serializers.CharField(required=True)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'book_name', 'book_author', 'title')


class PostCommentSwaggerRequestSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)
    parent = serializers.IntegerField(required=True)


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ('user', 'post', 'comment', 'parent')
        extra_kwargs = {
            'parent': {'required': False},
        }
    def validate(self, attrs):
        post_comment = PostComment.objects.filter(pk=attrs['parent'].id).first()
        if attrs['post'].id != post_comment.post.id:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Post id and parent id do not match')
        return attrs


class PostUpdateSwaggerRequestSerializer(serializers.Serializer):
    book_name = serializers.CharField(required=True)
    book_author = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=False)


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'book_name', 'book_author', 'title', 'is_active')
        extra_kwargs = {
            'user': {'required': True},
            'book_name': {'required': False},
            'book_author': {'required': False},
            'title': {'required': False},
            'is_active': {'required': False},
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
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'user', 'book_name', 'book_author', 'title', 'is_liked', 'like_count')
        read_only_fields = ('id', 'user')

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False


class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'user', 'book_name', 'book_author', 'title', 'is_liked', 'like_count', 'is_active', 'comments')
        read_only_fields = ('id', 'user')

    def get_comments(self, obj):
        comments = PostComment.objects.filter(post=obj, is_banned=False)
        return PostCommentListSerializer(comments, many=True, context=self.context).data

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False
