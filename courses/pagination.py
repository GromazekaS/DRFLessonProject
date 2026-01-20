from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    Кастомная пагинация с ограничением на максимальное количество элементов.
    """
    page_size = 3  # Количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр для изменения количества элементов на странице
    max_page_size = 10  # Максимальное количество элементов на странице
    page_query_param = 'page'  # Параметр для указания номера страницы

    def get_paginated_response(self, data):
        """
        Кастомизируем ответ пагинации для включения дополнительной информации.
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'results': data
        })