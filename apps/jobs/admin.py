from django.contrib import admin

from .models import Application, Job, Tag


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class Application(admin.ModelAdmin):
    pass
