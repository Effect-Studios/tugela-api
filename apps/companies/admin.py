from django.contrib import admin

from .models import Company, CompanyManager


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "email", "tagline", "phone_number")


admin.site.register(CompanyManager)
