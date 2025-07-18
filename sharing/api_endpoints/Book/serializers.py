from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from users.serializers import UserShortSerializer
from sharing.models import Book, Category
from shop.serializers import ShopShortSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'picture')


class BookBaseSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField(read_only=True)

    def get_percentage(self, obj):
        return obj.discount_percent

    def validate(self, attrs):
        price = attrs.get('price')
        discount_price = attrs.get('discount_price')

        if discount_price and price and discount_price > price:
            raise serializers.ValidationError(_('Discount price can not be greater than price'))

        return attrs


class BookCreateSerializer(BookBaseSerializer):
    class Meta:
        model = Book
        fields = (
            'id', 'picture', 'name', 'language', 'description', 'script_type', 'author',
            'cover_type', 'price', 'discount_price', 'publication_year', 'pages',
            'isbn', 'posted_by', 'shop', 'owner_type', 'percentage'
        )
        read_only_fields = ['posted_by', 'shop', 'owner_type']


class BookUpdateSerializer(BookBaseSerializer):
    class Meta:
        model = Book
        fields = (
            'id', 'picture', 'name', 'language', 'description', 'script_type', 'author',
            'cover_type', 'price', 'discount_price', 'publication_year', 'pages',
            'isbn'
        )
        extra_kwargs = {
            'name': {'required': False},
            'language': {'required': False},
            'description': {'required': False},
            'script_type': {'required': False},
            'author': {'required': False},
            'cover_type': {'required': False},
            'price': {'required': False},
            'discount_price': {'required': False},
            'publication_year': {'required': False},
            'pages': {'required': False},
            'isbn': {'required': False},
            'picture': {'required': False},
        }


class BookDetailSerializer(BookBaseSerializer):
    can_update = serializers.BooleanField(default=False)
    posted_by = UserShortSerializer(read_only=True)
    shop = ShopShortSerializer(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    view_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'picture', 'name', 'language', 'description', 'script_type', 'author',
            'cover_type', 'price', 'discount_price', 'publication_year', 'pages',
            'isbn', 'posted_by', 'shop', 'owner_type', 'percentage', 'can_update', 'created_at',
            'like_count', 'view_count', 'comment_count'
        )

    def get_like_count(self, obj):
        return obj.like_count

    def get_comment_count(self, obj):
        return obj.comment_count

    def get_view_count(self, obj):
        return obj.view_count


class BookListSerializer(BookBaseSerializer):
    posted_by = UserShortSerializer(read_only=True)
    shop = ShopShortSerializer(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    view_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'author', 'price', 'discount_price',
            'posted_by', 'shop', 'owner_type', 'percentage', 'like_count', 'view_count', 'created_at',
        )

    def get_like_count(self, obj):
        return obj.like_count

    def get_view_count(self, obj):
        return obj.view_count


class BookLikeSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
