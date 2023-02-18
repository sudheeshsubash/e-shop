from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'p'
    max_page_size = 2
    page_size_query_param = 2