from django.db import models

# from django.db.models import Count, Q


class FreelancerManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            # .annotate(
            #     total_applications=Count("applications"),
            #     accepted_applications=Count(
            #         "applications", filter=Q(applications__status="accepted")
            #     ),
            #     rejected_applications=Count(
            #         "applications", filter=Q(applications__status="rejected")
            #     ),
            # )
        )
