from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .paginators.posts_list_paginator import paginate_posts
from .models import Post, PostComment
from .serilalizers import (
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostDetailSerializer,
    PostParamValidateSerializer,
    PostCreateSwaggerRequestSerializer,
    PostUpdateSwaggerRequestSerializer,
    PostCommentCreateSerializer,
    PostCommentSwaggerRequestSerializer
)


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
        return Response(data={'result': 'Post deleted successfully', 'success': True, }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page_number', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter(
                'page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size'),
            openapi.Parameter(
                'is_popular', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Is popular'),
            openapi.Parameter(
                'q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search query')
        ],
        operation_summary='Posts list',
        operation_description='List of posts',
        responses={200: PostListSerializer(many=True)},
        tags=['Posts']
    )
    def post_list(self, request):
        param_serializer = PostParamValidateSerializer(data=request.query_params)
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message=param_serializer.errors)
        params = param_serializer.validated_data
        posts_filter = Q()
        if params.get('q'):
            query = params.get('q')
            posts_filter = Q(title__icontains=query) | Q(book_name__icontains=query) | Q(book_author__icontains=query)
        if params.get('is_popular') is True:
            three_days_ago = timezone.now() - timedelta(days=3)

            post_query = Post.objects.filter(created_at__gte=three_days_ago, is_active=True,
                                             is_banned=False).select_related("user").order_by('-like', '-created_at')
        else:
            post_query = Post.objects.filter(posts_filter, is_active=True,
                                             is_banned=False).select_related("user").order_by('-created_at__day', '-like')

        posts = paginate_posts(post_query, context={'request': request}, page_size=params.get('page_size'),
                               page_number=params.get('page_number'))

        return Response(data={'result': posts, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Posts detail',
        operation_description='Detail of a post',
        responses={200: PostDetailSerializer()},
        tags=['Posts']
    )
    def post_detail(self, request, pk=None):
        user = request.user
        post = Post.objects.filter(pk=pk, is_active=True, is_banned=False).select_related("user").first()
        if not post:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Post not found')
        post.views.add(user)
        serializer = PostDetailSerializer(post, context={'request': request})
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
        post_comment = PostComment.objects.filter(pk=pk, is_banned=False).first()
        if not post_comment:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Comment not found')
        user = request.user
        comment_liked = post_comment.like.filter(id=user.id).exists()
        if not comment_liked:
            post_comment.like.add(user)
        else:
            post_comment.like.remove(user)
        return Response(data={'result': not comment_liked, 'success': True}, status=status.HTTP_200_OK)
