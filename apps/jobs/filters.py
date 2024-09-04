from django_filters import rest_framework as filters

from .models import Application


class ApplicationFilter(filters.FilterSet):
    company = filters.CharFilter(field_name="job__company")

    class Meta:
        model = Application
        fields = ["freelancer", "job", "status", "company"]
