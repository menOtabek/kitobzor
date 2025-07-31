from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from utils.filters import BookFilter, SubCategoryFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from sharing.api_endpoints.Book.serializers import (
    BookCreateSerializer, BookUpdateSerializer, BookDetailSerializer,
    BookListSerializer, BookLikeSerializer, CategoryListSerializer, SubCategoryListSerializer,
)
from sharing.models import Book, BookLike, BookView, Category, SubCategory
from shop.models import Shop, ShopStuff
from utils.choices import OwnerType


@extend_schema(tags=["Book"])
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [BookFilter, OrderingFilter]

    def perform_create(self, serializer):
        user = self.request.user
        owned_shop = Shop.objects.filter(owner=user, is_active=True).first()
        staff_shop = ShopStuff.objects.filter(user=user, is_active=True).first()
        shop = owned_shop or (staff_shop.shop if staff_shop else None)
        owner_type = OwnerType.SHOP if shop else OwnerType.USER
        serializer.save(posted_by=user, shop=shop, owner_type=owner_type)

    @extend_schema(
        summary="Create a book",
        description="Create a new book entry (with optional file upload)",
        request=BookCreateSerializer,
        responses={201: BookDetailSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = BookCreateSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        self.perform_create(serializer)
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update a book",
        description="Update an existing book (partial allowed)",
        request=BookUpdateSerializer,
        responses={200: BookDetailSerializer}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.posted_by != request.user and not (instance.shop and instance.shop.owner == request.user):
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You can not update this book")
        serializer = BookUpdateSerializer(instance, data=request.data, partial=True, context={"request": request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete (ban) a book",
        description="Mark a book as banned instead of hard delete",
        responses={200: None}
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.posted_by != request.user and not (instance.shop and instance.shop.owner == request.user):
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You can only delete your own book.")
        instance.is_banned = True
        instance.save()
        return Response({'result': 'Book deleted', 'success': True}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve a book",
        description="Get detailed information about one book",
        responses={200: BookDetailSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        can_update = instance.posted_by == request.user or (instance.shop and instance.shop.owner == request.user)
        serializer = BookDetailSerializer(instance, context={"request": request})
        data = serializer.data
        data['can_update'] = can_update
        BookView.objects.create(user=request.user, book=instance)
        return Response({'result': data, 'success': True}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Book.objects.filter(is_banned=False).select_related('shop', 'posted_by')

    @extend_schema(
        summary="List books",
        description="List of books with filters",
        parameters=BookFilter.generate_query_parameters(),
        responses={200: BookListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = BookListSerializer(queryset, many=True, context={"request": request})
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @extend_schema(
        summary="List of liked books",
        description="Return a list of active, non-banned liked books",
        responses={200: BookListSerializer(many=True)}
    )
    def liked(self, request):
        books = Book.objects.filter(book_likes_count__user=request.user, is_active=True, is_banned=False)
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)



class BookLikeViewSet(ModelViewSet):
    serializer_class = BookLikeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @extend_schema(
        summary="Like a book",
        description="Like or unlike a book",
        request=BookLikeSerializer,
        tags=['Book']
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data['book_id']
        user = request.user

        like_object = BookLike.objects.filter(book_id=book_id, user=user)

        if like_object.exists():
            like_object.delete()
            return Response({"result": "Unliked", "success": True}, status=status.HTTP_200_OK)

        BookLike.objects.create(book_id=book_id, user=user)
        return Response({"result": "Liked", "success": True}, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Book"])
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="List all categories of book", responses={200: CategoryListSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


@extend_schema(tags=["Book"], parameters=SubCategoryFilter.generate_query_parameters())
class SubCategoryViewSet(ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SubCategoryFilter]

    @extend_schema(summary="List all subcategories of book", responses={200: SubCategoryListSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)
