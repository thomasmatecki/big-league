from api.leagues import models
from django.contrib import admin


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    pass


class SeasonLocationsInlineAdmin(admin.TabularInline):
    model = models.Season.locations.through


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ["name", "game_locations"]
