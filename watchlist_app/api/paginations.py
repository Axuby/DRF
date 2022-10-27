from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response

class WatchListPagination(PageNumberPagination):
    page_size = 5
    # page_query_params = 'p'
    page_size_query_param = 'size'
    max_page_size = 10
    # last_page_strings = 'end'

    def get_paginated_response(self, data):
        return Response({
            "links":{
                "next":self.get_next_link(),
                "previous":self.get_previous_link()

            },
            "count":self.page.paginator.count,
            "results":data
        })


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering = ['created_at', ]
    cursor_query_param = 'record'
