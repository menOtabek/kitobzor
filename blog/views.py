from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .models import Post, PostComment
from .serilalizers import (PostListSerializer,
                           PostCreateSerializer,
                           PostUpdateSerializer,
                           PostCommentCreateSerializer,
                           PostCommentListSerializer)

class PostViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_id='Posts create',
        operation_description='Create a new post',
        request_body=PostCreateSerializer,
        responses={201: PostListSerializer()},
        tags=['Posts']
    )
    def post_create(self, request):
        data = request.data
        data['user'] = request.user.id

        serializer = PostCreateSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Post update',
        operation_description='Update a post',
        request_body=PostUpdateSerializer,
        responses={200: PostListSerializer()},
        tags=['Posts']
    )
    def post_update(self, request, pk=None):
        post = Post.objects.filter(pk=pk, user=request.user).first()
        if not post:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Post not found')
        serializer = PostUpdateSerializer(instance=post, data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Post delete',
        operation_description='Delete a post',
        tags=['Posts']
    )
    def post_delete(self, request, pk=None):
        post = Post.objects.filter(pk=pk, user=request.user).first()
        if not post:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Post not found')
        post.delete()
        return Response(data={'result': 'Post deleted successfully', 'success': True,}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Posts list',
        operation_description='List of posts',
        responses={200: PostListSerializer(many=True)},
        tags=['Posts']
    )
    def post_list(self, request):
        posts = Post.objects.filter(is_active=True, is_banned=False)
        serializer = PostListSerializer(instance=posts, many=True)
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Posts detail',
        operation_description='Detail of a post',
        responses={200: PostListSerializer()},
        tags=['Posts']
    )
    def post_detail(self, request, pk=None):
        post = Post.objects.filter(pk=pk, is_active=True, is_banned=False).first()
        if not post:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Post not found')
        serializer = PostListSerializer(instance=post)
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)
