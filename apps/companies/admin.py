from django.contrib import admin

from .models import Company, CompanyIndustry, CompanyManager, CompanyValue


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "email", "tagline", "phone_number")


admin.site.register(CompanyManager)
admin.site.register(CompanyValue)
admin.site.register(CompanyIndustry)
