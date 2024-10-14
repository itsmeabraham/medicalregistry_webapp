from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class AppPagination(PageNumberPagination):
    """
    Pagination Class for deliveries endpoint
    """

    page_size = 50
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page": self.page.number,
                "per_page": self.get_page_size(self.request),
                "results": data,
            }
        )
