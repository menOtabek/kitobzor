from sharing.serializers import BookListSerializer
from django.core.paginator import Paginator

def paginate_books(books_query, context: dict, page_size: int, page_number: int):
    total_count = books_query.count()
    paginator = Paginator(books_query, page_size)
    books = paginator.get_page(page_number)

    response = {
        'total_elements': total_count,
        'total_pages': paginator.num_pages,
        'page_size': page_size,
        'current_page': page_number,
        'elements_number': len(books.object_list),
        'has_previous': books.has_previous(),
        'has_next': books.has_next(),
        'empty': total_count == 0,
        'content': BookListSerializer(books, many=True, context=context).data,
    }
    return response
