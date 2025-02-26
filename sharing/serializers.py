from rest_framework import serializers
from .models import Book, BookComment
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class BookParamValidateSerializer(serializers.Serializer):
    page_number = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=20)
    is_popular = serializers.BooleanField(required=False, default=False)
    q = serializers.CharField(required=False, default='')
    by_price = serializers.BooleanField(required=False, default=False)
    by_location = serializers.BooleanField(required=False, default=False)
    region_id = serializers.IntegerField(required=False)
    district_id = serializers.IntegerField(required=False)
    is_shop = serializers.BooleanField(required=True)

    def validate(self, attrs):
        if attrs.get('page_number') < 1 or attrs.get('page_size') < 1:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Page and page size must be positive integer')
        return attrs


class BookCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'author', 'picture', 'cover_type',
                  'price', 'pages', 'publication_year', 'isbn', 'description')
        extra_kwargs = {
            'description': {'required': False},
            'isbn': {'required': False},
        }


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'user', 'picture', 'name', 'description', 'author', 'cover_type',
                  'price', 'pages', 'publication_year', 'isbn')
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
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
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'picture', 'author', 'price', 'likes_count', 'views_count', 'pages', 'comments_count',
                  'publication_year', 'is_liked', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False


class BookCommentSwaggerSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)
    parent = serializers.IntegerField(required=False)


class BookCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment
        fields = ('id', 'user', 'book', 'comment', 'parent')
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
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
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookComment
        fields = ('id', 'user', 'book', 'comment', 'parent', 'likes_count', 'replies_count', 'is_liked', 'created_at')

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False


class BookDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'user', 'picture', 'name', 'description', 'author', 'cover_type', 'price', 'pages', 'is_active',
                  'publication_year', 'isbn', 'likes_count', 'is_liked', 'views_count', 'comments_count', 'created_at',
                  'updated_at', 'comments')

    def get_comments(self, obj):
        comments = BookComment.objects.filter(book=obj, is_banned=False)
        return BookCommentListSerializer(comments, many=True, context=self.context).data

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if obj.like.filter(id=user.id).exists():
            return True
        return False
