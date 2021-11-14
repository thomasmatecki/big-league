from api.leagues import models
from django_filters import filters, filterset


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class DefaultFilterSet(filterset.FilterSet):
    id = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.Team
        fields = ("id",)
