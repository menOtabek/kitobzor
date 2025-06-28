# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from exceptions.exception import CustomApiException
# from exceptions.error_messages import ErrorCodes
# from django.db.models import Q
# from .paginators.books_list_paginator import paginate_books
# from .models import Book, BookComment
# from .serializers import (
#     BookParamValidateSerializer, BookCreateSwaggerSerializer,
#     BookCreateSerializer, BookUpdateSerializer,
#     BookListSerializer, BookDetailSerializer,
#     BookCommentCreateSerializer, BookCommentListSerializer,
#     BookCommentSwaggerSerializer, BookUpdateSwaggerSerializer)
#
#
# class BookViewSet(viewsets.ViewSet):
#     @swagger_auto_schema(
#         operation_summary="Book create",
#         operation_description="Create a new book",
#         request_body=BookCreateSwaggerSerializer,
#         responses={status.HTTP_201_CREATED: BookCreateSerializer()},
#         tags=["Books"]
#     )
#     def create_a_book(self, request):
#         data = request.data
#         data['user'] = request.user.id
#         serializer = BookCreateSerializer(data=data, context={'request': request})
#         if not serializer.is_valid():
#             raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
#         serializer.save()
#         return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)
#
#     @swagger_auto_schema(
#         operation_summary="Book update",
#         operation_description="Update a book",
#         request_body=BookUpdateSwaggerSerializer,
#         responses={status.HTTP_200_OK: BookUpdateSerializer()},
#         tags=["Books"]
#     )
#     def update_a_book(self, request, pk):
#         data = request.data
#         data['user'] = request.user.id
#         book = Book.objects.filter(pk=pk, user_id=request.user.id, is_banned=False).first()
#         if not book:
#             raise CustomApiException(ErrorCodes.NOT_FOUND, message='Book not found')
#         serializer = BookUpdateSerializer(instance=book, data=request.data, partial=True, context={'request': request})
#         if not serializer.is_valid():
#             raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
#         serializer.save()
#         return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         operation_summary="Book details",
#         operation_description="Get a book",
#         responses={status.HTTP_200_OK: BookDetailSerializer()},
#         tags=["Books"]
#     )
#     def get_a_book(self, request, pk):
#         book = Book.objects.filter(pk=pk, is_banned=False).select_related("user").first()
#         if not book:
#             raise CustomApiException(ErrorCodes.NOT_FOUND, message='Book not found')
#         serializer = BookDetailSerializer(book, context={'request': request})
#         return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         operation_summary="Book delete",
#         operation_description="Delete a book",
#         tags=["Books"]
#     )
#     def delete_a_book(self, request, pk):
#         book = Book.objects.filter(pk=pk, user_id=request.user.id, is_banned=False).first()
#         if not book:
#             raise CustomApiException(ErrorCodes.NOT_FOUND, message='Book not found')
#         book.is_banned = True
#         book.save(update_fields=['is_banned'])
#         return Response(data={'result': 'Book deleted successfully', 'success': True}, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         operation_summary="Book like | dislike",
#         operation_description="Like or dislike a book",
#         tags=["Books"]
#     )
#     def like_a_book(self, request, pk):
#         book = Book.objects.filter(pk=pk, is_banned=False).first()
#         if not book:
#             raise CustomApiException(ErrorCodes.NOT_FOUND, message='Book not found')
#         user = request.user
#         liked_book = book.like.filter(id=user.id).exists()
#         if not liked_book:
#             book.like.add(user)
#         else:
#             book.like.remove(user)
#         return Response(data={'result': not liked_book, 'success': True}, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'page_number', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
#             openapi.Parameter(
#                 'page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size'),
#             openapi.Parameter(
#                 'is_popular', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Is popular'),
#             openapi.Parameter(
#                 'q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search query'),
#             openapi.Parameter(
#                 'by_price', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='By price'),
#             openapi.Parameter(
#                 'by_location', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='By location'),
#             openapi.Parameter(
#                 'region_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='In region'),
#             openapi.Parameter(
#                 'district_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='In district'),
#             openapi.Parameter(
#                 'is_shop', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Is shop')
#         ],
#         operation_summary="Books list",
#         operation_description="Get list of books",
#         responses={status.HTTP_200_OK: BookListSerializer()},
#         tags=["Books"]
#     )
#     def books_list(self, request):
#         query_serializer = BookParamValidateSerializer(data=request.query_params)
#         if not query_serializer.is_valid():
#             raise CustomApiException(ErrorCodes.INVALID_INPUT, query_serializer.errors)
#         book_filter = Q()
#         query = query_serializer.validated_data
#
#         if query.get('q'):
#             book_filter &= Q(name__icontains=query.get('q')) | Q(author__icontains=query.get('q'))
#         if query.get('region_id'):
#             book_filter &= Q(user__region_id=query.get('region_id'))
#         if query.get('district_id'):
#             book_filter &= Q(user__district_id=query.get('district_id'))
#         if query.get('is_shop') is True:
#             if query.get('is_popular') is True:
#                 books_query = Book.objects.filter(user__role=3, is_active=True, is_banned=False
#                 ).order_by( '-created_at')[:20]
#
#             elif query.get('by_location') is True:
#                 books_query = Book.objects.filter(
#                     book_filter, user__role=3, is_active=True, is_banned=False).order_by('-created_at')
#
#             elif query.get('by_price') is True:
#                 books_query = Book.objects.filter(
#                     book_filter, user__role=3, is_active=True, is_banned=False).order_by('-price', '-created_at')
#             else:
#                 books_query = Book.objects.filter(
#                     book_filter, user__role=3, is_active=True, is_banned=False).order_by('-created_at')
#             books = paginate_books(books_query, context={'request': request}, page_size=query.get('page_size'),
#                                    page_number=query.get('page_number'))
#         else:
#             if query.get('is_popular') is True:
#                 books_query = Book.objects.filter(is_active=True, user__role=4,
#                     is_banned=False).order_by( '-created_at')[:20]
#
#             elif query.get('by_location') is True:
#                 books_query = Book.objects.filter(
#                     book_filter, is_active=True, user__role=4, is_banned=False).order_by('-created_at')
#
#             elif query.get('by_price') is True:
#                 books_query = Book.objects.filter(
#                     book_filter, is_active=True, user__role=4, is_banned=False).order_by('-price', '-created_at')
#             else:
#                 books_query = Book.objects.filter(
#                     book_filter, is_active=True, user__role=4, is_banned=False).order_by('-created_at')
#             books = paginate_books(books_query, context={'request': request}, page_size=query.get('page_size'),
#                                    page_number=query.get('page_number'))
#         return Response(data={'result': books, 'success': True}, status=status.HTTP_200_OK)
#
#
# class BookCommentViewSet(viewsets.ViewSet):
#     @swagger_auto_schema(
#         operation_summary='Book comment create',
#         operation_description='Create a new book comment',
#         request_body=BookCommentSwaggerSerializer,
#         responses={status.HTTP_201_CREATED: BookCommentListSerializer()},
#         tags=['Book Comment']
#     )
#     def create_a_book_comment(self, request, pk):
#         book = Book.objects.filter(pk=pk, is_active=True, is_banned=False).first()
#         if not book:
#             raise CustomApiException(ErrorCodes.NOT_FOUND, 'Book not found')
#         data = request.data
#         data['user'] = request.user.id
#         data['book'] = book.id
#         serializer = BookCommentCreateSerializer(data=data, context={'request': request})
#         if not serializer.is_valid():
#             raise CustomApiException(ErrorCodes.INVALID_INPUT, message=serializer.errors)
#         serializer.save()
#         return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)
#
#     @swagger_auto_schema(
#         operation_summary='Book comment delete',
#         operation_description='Delete a book comment',
#         tags=['Book Comment']
#     )
#     def delete_a_book_comment(self, request, pk):
#         user = request.user
#         comment = BookComment.objects.filter(pk=pk, user=user, is_banned=False).first()
#         if not comment:
#             raise CustomApiException(ErrorCodes.NOT_FOUND, message='Comment not found')
#         comment.is_banned = True
#         comment.save(update_fields=['is_banned'])
#         return Response(data={'result': 'Comment deleted successfully', 'success': True}, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         operation_summary='Book comment like | dislike',
#         operation_description='Like or dislike a book comment',
#         tags=['Book Comment']
#     )
#     def like_a_book_comment(self, request, pk=None):
#         book_comment = BookComment.objects.filter(pk=pk, is_banned=False).first()
#         if not book_comment:
#             raise CustomApiException(ErrorCodes.NOT_FOUND, message='Comment not found')
#         user = request.user
#         liked_comment = book_comment.like.filter(id=user.id).exists()
#         if liked_comment:
#             book_comment.like.remove(user)
#         else:
#             book_comment.like.add(user)
#         return Response(data={'result': not liked_comment, 'success': True}, status=status.HTTP_200_OK)


# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from drf_spectacular.utils import extend_schema, OpenApiParameter
#
# from .models import Book, BookView
# from .serializers import BookSerializer, BookDetailSerializer
#
#
# @extend_schema(tags=["Books"])
# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.filter(is_banned=False).order_by('-created_at')
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return BookDetailSerializer
#         return BookSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(posted_by=self.request.user)
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if request.user.is_authenticated:
#             BookView.objects.get_or_create(user=request.user, book=instance)
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.is_banned = True
#         instance.save()
#         return Response({"detail": "Book banned (soft deleted)."}, status=status.HTTP_204_NO_CONTENT)
