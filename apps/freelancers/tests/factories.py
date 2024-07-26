import factory
from factory import Faker
from factory.django import DjangoModelFactory

from apps.freelancers.models import Freelancer, PortfolioItem, Service, WorkExperience
from apps.users.tests.factories import CategoryFactory, SkillFactory, UserFactory


class FreelancerFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Freelancer


class WorkExperienceFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    freelancer = factory.SubFactory(FreelancerFactory)
    job_title = Faker("job")
    company_name = Faker("company")
    start_date = Faker("date_this_month")

    class Meta:
        model = WorkExperience


class PortfolioItemFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    freelancer = factory.SubFactory(FreelancerFactory)
    category = factory.SubFactory(CategoryFactory)
    skills = factory.RelatedFactory(
        SkillFactory
    )  # Use RelatedFactory for many to many fields
    title = Faker("job")
    portfolio_file = Faker("file_path")
    start_date = Faker("date_this_month")

    class Meta:
        model = PortfolioItem
        skip_postgeneration_save = True


class ServiceFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    freelancer = factory.SubFactory(FreelancerFactory)
    category = factory.SubFactory(CategoryFactory)
    skills = factory.RelatedFactory(
        SkillFactory
    )  # Use RelatedFactory for many to many fields
    title = Faker("job")
    price_type = Faker("word", ext_word_list=["per_hour", "per_project"])

    class Meta:
        model = Service
        skip_postgeneration_save = True
