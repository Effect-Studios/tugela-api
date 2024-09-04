from django.db import models

# from django.db.models import Count, Q


class CompanyManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            # .annotate(
            #     total_jobs=Count("jobs"),
            #     active_jobs=Count("jobs", filter=Q(jobs__status="active")),
            #     assigned_jobs=Count("jobs", filter=Q(jobs__status="assigned")),
            #     completed_jobs=Count("jobs", filter=Q(jobs__status="completed")),
            #     total_applications=Count("jobs__applicants"),
            # )
        )
