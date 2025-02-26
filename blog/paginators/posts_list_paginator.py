from blog.serilalizers import PostListSerializer
from django.core.paginator import Paginator

def paginate_posts(post_query, context: dict, page_size: int, page_number: int):
    total_count = post_query.values('id').distinct().count()

    paginator = Paginator(post_query, page_size)
    posts = paginator.get_page(page_number)

    response = {
        'total_elements': total_count,
        'total_pages': paginator.num_pages,
        'page_size': page_size,
        'current_page': page_number,
        'elements_number': len(posts.object_list),
        'has_previous': posts.has_previous(),
        'has_next': posts.has_next(),
        'empty': total_count == 0,
        'content': PostListSerializer(posts, many=True, context=context).data,
    }
    return response
