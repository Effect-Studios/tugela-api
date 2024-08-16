from django.contrib import admin

from .models import Country, Currency

# Register your models here.


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "code", "name"]
    list_display = ["name", "code", "symbol", "_type"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "code", "name", "iso"]
    list_display = ["name", "iso", "code"]
