from django.contrib import admin

from .models import Freelancer, PortfolioItem, Service, WorkExperience

admin.site.register(Freelancer)
admin.site.register(WorkExperience)
admin.site.register(PortfolioItem)
admin.site.register(Service)
