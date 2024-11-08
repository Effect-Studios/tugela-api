from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.common.pagination import DefaultPagination

from .serializers import JobScoreSerializer
from .utils import get_job_score_json

job_score_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "score": openapi.Schema(type=openapi.TYPE_STRING),
        "confidence_score": openapi.Schema(type=openapi.TYPE_STRING),
        "Technical Skills and Competency": openapi.Schema(type=openapi.TYPE_STRING),
        "Cultural Fit and Behavioral Traits": openapi.Schema(type=openapi.TYPE_STRING),
        "Experience and Potential": openapi.Schema(type=openapi.TYPE_STRING),
        "explanation": openapi.Schema(type=openapi.TYPE_STRING),
    },
)


class AIView(ViewSet, DefaultPagination):
    @swagger_auto_schema(method="POST", responses={200: job_score_response_schema})
    @action(
        detail=False,
        permission_classes=[AllowAny],
        methods=["POST"],
        url_path="job-score",
    )
    def job_score(self, request):
        serializer = JobScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        freelancer = serializer.validated_data.get("freelancer")
        job = serializer.validated_data.get("job")

        freelancer_skills = freelancer.skills.values_list("name", flat=True)
        job_description = f"{job.description}. {job.responsibilities}. {job.experience}"

        res = get_job_score_json(freelancer_skills, job_description)

        return Response(res)
