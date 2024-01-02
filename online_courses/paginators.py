from rest_framework.pagination import PageNumberPagination


class OnlineCoursePaginator(PageNumberPagination):
    """ Пагинация для вывода списков курсов и уроков."""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100
