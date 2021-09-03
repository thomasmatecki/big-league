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
from rest_framework.schemas import get_schema_view

from api import router
from api.core.rest import DefaultSchemaGenerator
from api.core.views import UserViewSet
from api.leagues.views import LeagueViewSet, PlayerViewSet, SeasonViewSet, TeamViewSet

router.register("users", UserViewSet)
router.register("players", PlayerViewSet)
router.register("teams", TeamViewSet)
router.register("seasons", SeasonViewSet)
router.register("leagues", LeagueViewSet)


schema_view = get_schema_view(
    title="API", 
    url="",
    generator_class=DefaultSchemaGenerator
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("rest/", include((router.urls))),
    path("schema/", schema_view),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]
