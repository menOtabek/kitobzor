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
                           PostCreateSwaggerRequestSerializer,
                           PostUpdateSwaggerRequestSerializer,
                           PostCommentCreateSerializer,
                           PostCommentSwaggerRequestSerializer)

class PostViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_id='Posts create',
        operation_description='Create a new post',
        request_body=PostCreateSwaggerRequestSerializer,
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
        request_body=PostUpdateSwaggerRequestSerializer,
        responses={200: PostListSerializer()},
        tags=['Posts']
    )
    def post_update(self, request, pk=None):
        post = Post.objects.filter(pk=pk, user=request.user).first()
        if not post:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Post not found')
        data = request.data
        data['user'] = request.user.id
        serializer = PostUpdateSerializer(instance=post, data=data, context={'request': request})
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
        post.is_banned = True
        post.save(update_fields=['is_banned'])
        return Response(data={'result': 'Post deleted successfully', 'success': True,}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Posts list',
        operation_description='List of posts',
        responses={200: PostListSerializer(many=True)},
        tags=['Posts']
    )
    def post_list(self, request):
        posts = Post.objects.filter(is_active=True, is_banned=False)
        serializer = PostListSerializer(instance=posts, many=True, context={'request': request})
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
        serializer = PostListSerializer(instance=post, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Post like | dislike',
        operation_description='Like or dislike a post',
        tags=['Posts']
    )
    def post_like(self, request, pk=None):
        user = request.user
        post = Post.objects.filter(pk=pk, is_active=True, is_banned=False).first()
        if not post:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Post not found')
        liked = post.like.filter(id=user.id).exists()
        if not liked:
            post.like.add(user)
        else:
            post.like.remove(user)
        return Response(data={'result': not liked, 'success': True}, status=status.HTTP_200_OK)


class PostCommentViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary='Comment create',
        operation_description='Create a new comment by post id',
        request_body=PostCommentSwaggerRequestSerializer,
        responses={201: PostCommentCreateSerializer()},
        tags=['PostComments']
    )
    def post_comment_create(self, request, pk=None):
        post = Post.objects.filter(pk=pk, is_active=True, is_banned=False).first()
        if not post:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Post not found')
        data = request.data
        data['user'] = request.user.id
        data['post'] = post.id
        serializer = PostCommentCreateSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Comment delete',
        operation_description='Delete a comment',
        tags=['PostComments']
    )
    def post_comment_delete(self, request, pk=None):
        comment = PostComment.objects.filter(pk=pk, user_id=request.user.id, is_banned=False).first()
        if not comment:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Comment not found')
        comment.is_banned = True
        comment.save(update_fields=['is_banned'])
        return Response(data={'result': 'Comment deleted successfully', 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Comment like | dislike',
        operation_description='Like or dislike a comment',
        tags=['PostComments']
    )
    def post_comment_like(self, request, pk=None):
        user = request.user
        comment = PostComment.objects.filter(pk=pk, is_banned=False).first()
        comment_liked = comment.like.filter(id=user.id).exists()
        if not comment:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Comment not found')
        if not comment_liked:
            comment.like.add(user)
        else:
            comment.like.remove(user)
        return Response(data={'result': not comment_liked, 'success': True}, status=status.HTTP_200_OK)
