from rest_framework import serializers

from apps.freelancers.models import Freelancer
from apps.jobs.models import Job


class JobScoreSerializer(serializers.Serializer):
    freelancer = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all())
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
