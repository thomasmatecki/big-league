"""dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from api.core.rest import DefaultSchemaGenerator
from api.core.views import SessionViewSet, UserViewSet
from api.leagues.views import (
    AttendanceViewSet,
    LeagueViewSet,
    MatchViewSet,
    PlayerViewSet,
    ProfileViewSet,
    ScheduleViewSet,
    SeasonViewSet,
    TeamViewSet,
)

router = DefaultRouter()

router.register("users", UserViewSet)
router.register("players", PlayerViewSet)
router.register("teams", TeamViewSet)
router.register("seasons", SeasonViewSet)
router.register("leagues", LeagueViewSet)
# router.register("sessions", SessionViewSet)
router.register("matches", MatchViewSet)
router.register("attendance", AttendanceViewSet, basename="attendance")


schema_view = get_schema_view(
    title="API", url="", generator_class=DefaultSchemaGenerator
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("rest/", include((router.urls))),
    path(
        "user/profile/",
        ProfileViewSet.as_view(
            actions={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "post": "create",
            }
        ),
    ),
    path("user/schedule/", ScheduleViewSet.as_view({"get": "list"})),
    path("user/session/", SessionViewSet.as_view({"get": "retrieve", "put": "update"})),
    path("schema/", schema_view),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]
