from django_filters import rest_framework as filters

from .models import Application, JobSubmission


class ApplicationFilter(filters.FilterSet):
    company = filters.CharFilter(field_name="job__company")

    class Meta:
        model = Application
        fields = ["freelancer", "job", "status", "company"]


class JobSubmissionFilter(filters.FilterSet):
    company = filters.CharFilter(field_name="application__job__company")

    class Meta:
        model = JobSubmission
        fields = ["freelancer", "application", "company"]
