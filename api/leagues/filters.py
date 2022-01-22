from api.leagues import models
from django.forms.widgets import Select
from django_filters import filters, filterset


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class DefaultFilterSet(filterset.FilterSet):
    id = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.Team
        fields = ("id",)


TAILWIND_ATTRS = {
    "class": "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
}


def leagues(request):
    return models.League.objects.all()


class SeasonFilter(filterset.FilterSet):
    league = filterset.ModelChoiceFilter(
        queryset=leagues, widget=Select(attrs=TAILWIND_ATTRS)
    )

    location = filterset.ModelChoiceFilter(
        queryset=models.Location.objects.all(),
        field_name="locations",
        widget=Select(attrs=TAILWIND_ATTRS),
    )

    class Meta:
        model = models.Season
        fields = ["league", "location"]
