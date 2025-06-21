from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from blog.models import Post
from blog.Post.serializers import (
    PostCreateSerializer,
    PostUpdateSerializer,
    PostListSerializer,
    PostDetailSerializer
)


@extend_schema(tags=["Post"])
class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_banned=False).select_related('user').order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action == 'list':
            return PostListSerializer
        return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Create a post",
        request=PostCreateSerializer,
        responses={201: PostCreateSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        self.perform_create(serializer)
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update your post",
        responses={200: PostUpdateSerializer}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You can only update your own post.")

        serializer = self.get_serializer(instance, data=request.data, partial=True, context={"request": request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="List posts",
        parameters=[
            OpenApiParameter(name='book_name', type=OpenApiTypes.STR, required=False, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='book_author', type=OpenApiTypes.STR, required=False, location=OpenApiParameter.QUERY)
        ],
        responses={200: PostListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_active=True)

        book_name = request.query_params.get('book_name')
        book_author = request.query_params.get('book_author')

        if book_name:
            queryset = queryset.filter(book_name__icontains=book_name)
        if book_author:
            queryset = queryset.filter(book_author__icontains=book_author)

        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Get post detail",
        responses={200: PostDetailSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @extend_schema(summary="Delete (ban) your post", responses={200: None})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You can only delete your own post.")
        instance.is_banned = True
        instance.save(update_fields=['is_banned'])
        return Response({'result': 'Post banned successfully.', 'success': True}, status=status.HTTP_200_OK)
