from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from sharing.api_endpoints.Book.serializers import BookLikeSerializer
from sharing.api_endpoints.BookComment.serializers import BookCommentSerializer, BookCommentLikeSerializer
from sharing.models import BookComment, BookCommentLike


@extend_schema(tags=["BookComment"])
class BookCommentViewSet(ModelViewSet):
    queryset = BookComment.objects.filter(is_banned=False).select_related('user', 'book', 'parent')
    serializer_class = BookCommentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List book comments",
        description="List all top-level comments for a specific book",
        responses={200: BookCommentSerializer(many=True)},
        tags=["BookComment"],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_banned=False).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    def get_queryset(self):
        book_id = self.request.query_params.get('book')
        queryset = self.queryset.filter(parent__isnull=True).order_by('-created_at')
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Create a new book comment",
        request=BookCommentSerializer,
        responses={201: BookCommentSerializer},
        tags=["BookComment"],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        self.perform_create(serializer)
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Delete (ban) your comment",
        responses={200: None},
        tags=["BookComment"],
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You can only delete your own comment.")
        instance.is_banned = True
        instance.save(update_fields=['is_banned'])
        return Response({'result': 'Comment banned', 'success': True}, status=status.HTTP_200_OK)


class BookLikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @extend_schema(
        summary="Like a book comment",
        description="Like or unlike a book comment",
        request=BookCommentLikeSerializer,
        tags=['BookComment'],
    )
    def create(self, request, *args, **kwargs):
        serializer = BookCommentLikeSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        user = request.user
        comment_id = serializer.validated_data['comment_id']

        if BookCommentLike.objects.filter(comment_id=comment_id, user=user).exists():
            BookCommentLike.objects.filter(comment_id=comment_id, user=user).delete()
            return Response({"result": "Unliked", 'success': True}, status=status.HTTP_200_OK)
        else:
            BookCommentLike.objects.create(comment_id=comment_id, user=user)
            return Response({"result": "Liked", 'success': True}, status=status.HTTP_201_CREATED)
