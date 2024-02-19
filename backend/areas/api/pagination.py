from rest_framework.pagination import PageNumberPagination


class CommentPaginator(PageNumberPagination):
    """
    Пагинатор с возможностью устанавливать кол-во комментариев на страницу.
    """
    page_size_query_param = 'limit'
    page_size = 5
