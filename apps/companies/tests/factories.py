import factory
from factory import Faker
from factory.django import DjangoModelFactory

from apps.companies.models import Company, CompanyManager
from apps.users.tests.factories import UserFactory


class CompanyFactory(DjangoModelFactory):
    name = Faker("company")
    user = factory.SubFactory(UserFactory)
    organization_type = Faker("word", ext_word_list=["public_company", "self_employed"])

    class Meta:
        model = Company


class CompanyManagerFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)

    class Meta:
        model = CompanyManager
