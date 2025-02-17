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
        fields = ('user', 'book_name', 'book_author', 'title')
        extra_kwargs = {
            'user': {'read_only': True},
            'book_name': {'required': False},
            'book_author': {'required': False},
            'title': {'required': False},
        }

        def update(self, instance, validated_data):
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance
