from django.contrib import admin

from .models import Application, Job, JobSubmission, Tag


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class Application(admin.ModelAdmin):
    pass


@admin.register(JobSubmission)
class JobSubmissionAdmin(admin.ModelAdmin):
    search_fields = [
        "application.job.title",
        "application.freelancer.user.username",
        "application.freelancer.user.email",
        "application.freelancer.fullname",
    ]
