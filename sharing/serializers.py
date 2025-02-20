from rest_framework import serializers
from .models import Book, BookComment
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class PostParamValidateSerializer(serializers.Serializer):
    page_number = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    is_popular = serializers.BooleanField(required=False, default=False)
    q = serializers.CharField(required=False, default='')
    by_price = serializers.BooleanField(required=False, default=False)
    by_location = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        if attrs.get('page_number') < 1 or attrs.get('page_size') < 1:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Page and page size must be positive integer')
        return attrs


class BookSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('picture', 'name', 'description', 'author', 'cover_type',
                  'price', 'pages', 'publication_year', 'isbn', 'is_active')
        extra_kwargs = {
            'description': {'required': False},
            'isbn': {'required': False},
        }


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('user', 'picture', 'name', 'description', 'author', 'cover_type',
                  'price', 'pages', 'publication_year', 'isbn')
        extra_kwargs = {
            'description': {'required': False},
            'isbn': {'required': False},
        }


class BookUpdateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('picture', 'name', 'description', 'author', 'cover_type',
                  'price', 'pages', 'publication_year', 'isbn', 'is_active')
        extra_kwargs = {
            'picture': {'required': False},
            'name': {'required': False},
            'description': {'required': False},
            'author': {'required': False},
            'cover_type': {'required': False},
            'price': {'required': False},
            'pages': {'required': False},
            'publication_year': {'required': False},
            'isbn': {'required': False},
            'is_active': {'required': False},
        }


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('user', 'picture', 'name', 'description', 'author', 'cover_type',
                  'price', 'pages', 'publication_year', 'isbn', 'is_active')
        extra_kwargs = {
            'user': {'required': True},
            'picture': {'required': False},
            'name': {'required': False},
            'description': {'required': False},
            'author': {'required': False},
            'cover_type': {'required': False},
            'price': {'required': False},
            'pages': {'required': False},
            'publication_year': {'required': False},
            'isbn': {'required': False},
            'is_active': {'required': False},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'price', 'likes_count', 'pages', 'publication_year', 'is_liked')


class BookCommentSwaggerSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)
    parent = serializers.IntegerField(required=False)


class BookCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment
        fields = ('user', 'book', 'comment', 'parent')
        extra_kwargs = {
            'parent': {'required': False},
        }

    def validate(self, attrs):
        if attrs.get('parent'):
            book_comment = BookComment.objects.filter(pk=attrs['parent'].id).first()
            if attrs['book'].id != book_comment.book.id:
                raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Book id and comment id do not match')
            return attrs
        return attrs


class BookCommentListSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    replies_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = BookComment
        fields = ('id', 'user', 'book', 'comment', 'parent', 'likes_count', 'replies_count', 'is_liked')

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False


class BookDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True, default=False)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'user', 'picture', 'name', 'description', 'author', 'cover_type', 'price', 'pages', 'is_active',
                  'publication_year', 'isbn', 'likes_count', 'is_liked', 'views_count', 'comments_count', 'comments')

    def get_comments(self, obj):
        comments = BookComment.objects.filter(book=obj, is_banned=False)
        return BookCommentListSerializer(comments, many=True, context=self.context).data

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False
