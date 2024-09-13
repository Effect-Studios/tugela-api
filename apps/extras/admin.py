from django.contrib import admin

from .models import Country, Currency, PaymentService

# Register your models here.


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ["id", "code", "name"]
    list_display = ["name", "code", "symbol", "_type"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ["id", "code", "name", "iso"]
    list_display = ["name", "iso", "code"]


@admin.register(PaymentService)
class PaymentServiceAdmin(admin.ModelAdmin):
    search_fields = ["id", "name", "url"]
    list_display = ["name", "url"]
