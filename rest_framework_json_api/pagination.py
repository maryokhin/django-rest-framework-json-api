"""
Pagination fields
"""
from collections import OrderedDict

from rest_framework.pagination import BasePagination, PageNumberPagination as DRFPageNumberPagination
from rest_framework.templatetags.rest_framework import replace_query_param
from rest_framework.views import Response


class JSONApiPagination(BasePagination):
    """
    JSON API specification defines that the following keys
    MUST be used for pagination: `first`, `last`, `next`, `previous`.
    Those keys MUST be present in the `links` section.

    Therefore it is mandatory for any JSON API pagination style to define the links
    or return `None` if they are not relevant for a specific pagination style.

    http://jsonapi.org/format/#fetching-pagination
    """

    def get_first_link(self):
        raise NotImplementedError('get_first_link() must be implemented.')

    def get_last_link(self):
        raise NotImplementedError('get_last_link() must be implemented.')

    def get_next_link(self):
        raise NotImplementedError('get_next_link() must be implemented.')

    def get_previous_link(self):
        raise NotImplementedError('get_previous_link() must be implemented.')

    def get_pagination_links(self):
        return OrderedDict([
            ('first', self.get_first_link()),
            ('last', self.get_last_link()),
            ('next', self.get_next_link()),
            ('prev', self.get_previous_link()),
        ])

    def get_pagination_meta(self):
        raise NotImplemented('get_pagination_meta() must be implemented.')

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'meta': {
                'pagination': self.get_pagination_meta()
            },
            'links': self.get_pagination_links()
        })


class PageNumberPagination(JSONApiPagination, DRFPageNumberPagination):
    """
    A json-api compatible pagination format.
    """

    page_size_query_param = 'page_size'
    max_page_size = 100

    def build_link(self, index):
        if not index:
            return None
        url = self.request and self.request.build_absolute_uri() or ''
        return replace_query_param(url, 'page', index)

    def get_first_link(self):
        return self.build_link(1)

    def get_last_link(self):
        return self.build_link(self.page.paginator.num_pages)

    def get_next_link(self):
        return DRFPageNumberPagination.get_next_link(self)

    def get_previous_link(self):
        return DRFPageNumberPagination.get_previous_link(self)

    def get_pagination_meta(self):
        return OrderedDict([
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
        ])
