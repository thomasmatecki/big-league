
from api.leagues.filters import SeasonFilter
from api.leagues.models import Schedule, Season
from api.leagues.views import SeasonViewSet
from django.views.generic import TemplateView


class ScheduleView(TemplateView):
    template_name = "schedule.html"

    @property
    def extra_context(self):
        return {"schedule": Schedule.objects.all()}


class SeasonListView(TemplateView):
    def __init__(self, **kwargs) -> None:
        self.rest_view = SeasonViewSet(**kwargs)
        super().__init__(**kwargs)

    template_name = "league-list.html"

    @property
    def extra_context(self):
        filter_ = SeasonFilter(self.request.GET, queryset=Season.objects.all())
        return {
            "form": filter_.form,
            "results": filter_.qs,
            "list_template": self.rest_view.template_name
        }
