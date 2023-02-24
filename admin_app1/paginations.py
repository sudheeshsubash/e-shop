from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    '''
    custom paginations
    '''
    page_size = 2
    page_query_param = 'page'
    max_page_size = 5
    page_size_query_param = 'pagesize'