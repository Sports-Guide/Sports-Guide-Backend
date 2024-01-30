from django_filters import rest_framework as filters

from areas.models import Category


class AreaFilter(filters.FilterSet):
    """Фильтр поиска по категории."""

    categories = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='categories__slug',
        to_field_name='slug',
    )
