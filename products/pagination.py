from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPageNumberPagination(pagination.PageNumberPagination):
    def get_page_size(self, request):
        if request.user.is_staff:  #Admins have different page_size
            return 1000
        else:
            return 100


    page_size = 100
    page_size_query_param = 'count'
    max_page_size = 1000
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data, **kwargs):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]),
        **kwargs
        )
