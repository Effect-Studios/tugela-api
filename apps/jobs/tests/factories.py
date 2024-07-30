import factory
from factory import Faker
from factory.django import DjangoModelFactory

from apps.companies.tests.factories import CompanyFactory
from apps.freelancers.tests.factories import FreelancerFactory
from apps.jobs.models import Application, Job, Tag


class TagFactory(DjangoModelFactory):
    name = Faker("word")

    class Meta:
        model = Tag


class JobFactory(DjangoModelFactory):
    title = Faker("job")
    company = factory.SubFactory(CompanyFactory)
    price_type = Faker("word", ext_word_list=["per_hour", "per_project"])
    tags = factory.RelatedFactory(TagFactory)

    class Meta:
        model = Job


class ApplicationFactory(DjangoModelFactory):
    freelancer = factory.SubFactory(FreelancerFactory)
    job = factory.SubFactory(JobFactory)

    class Meta:
        model = Application
