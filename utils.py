"""Вспомогательные функции для проекта"""

from django.core.paginator import Paginator

def paginate_queryset(request, queryset, items_per_page=12):
    """Пагинация для любого набора данных"""
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)