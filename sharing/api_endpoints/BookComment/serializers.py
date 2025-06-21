from rest_framework import serializers

from authentication.serializers import UserShortSerializer
from sharing.models import BookComment


class BookCommentReplySerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = BookComment
        fields = ('id', 'user', 'comment', 'created_at')
        read_only_fields = ('created_at', 'user')


class BookCommentSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    replies = BookCommentReplySerializer(many=True, read_only=True)

    class Meta:
        model = BookComment
        fields = (
            'id', 'user', 'book', 'comment',
            'parent', 'replies', 'created_at'
        )
        read_only_fields = ('user', 'replies')


class BookCommentLikeSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
