from cProfile import label

import django_filters
from api.leagues.models import League, Location, Schedule, Season
from django.forms.widgets import Select
from django.views.generic import TemplateView


class ScheduleView(TemplateView):
    template_name = "schedule.html"

    @property
    def extra_context(self):
        return {"schedule": Schedule.objects.all()}


def leagues(request):
    return League.objects.all()


TAILWIND_ATTRS = {
    "class": "mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
}


class SeasonFilter(django_filters.FilterSet):
    league = django_filters.ModelChoiceFilter(
        queryset=leagues, widget=Select(attrs=TAILWIND_ATTRS)
    )

    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.all(),
        field_name="locations",
        widget=Select(attrs=TAILWIND_ATTRS),
    )

    class Meta:
        model = Season
        fields = ["league", "location"]


class SeasonListView(TemplateView):
    template_name = "league-list.html"

    @property
    def extra_context(self):
        filter_ = SeasonFilter(self.request.GET, queryset=Season.objects.all())
        return {"filter": filter_}
