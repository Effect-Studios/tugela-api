import pytest
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


User = get_user_model()


class TestCompany:
    def test_list_company(self, api_client_auth, admin, user: User, company_factory):
        url = reverse("api:company-list")
        company_factory.create_batch(3, user=user)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_company(self, api_client_auth, user):
        url = reverse("api:company-list")
        client = api_client_auth(user=user)
        data = {
            "user": str(user.id),
            "name": "company",
            "organization_type": "public_company",
        }

        resp = client.post(url, data=data)
        resp_data = resp.json()

        user.refresh_from_db()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["user"] == data["user"]
        assert user.role == user.Roles.OWNER

    def test_update_company(self, api_client_auth, user, company_factory):
        company = company_factory(user=user)
        url = reverse("api:company-detail", args=(company.id,))
        data = {"name": "Updated company"}

        client = api_client_auth(user=user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["name"] == data["name"]

    def test_read_comapny(self, api_client_auth, user, company_factory):
        company = company_factory(user=user)
        url = reverse("api:company-detail", args=(company.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["name"] == company.name


class TestCompanyManager:
    def test_list_company_manger(
        self,
        api_client_auth,
        admin,
        user: User,
        company_factory,
        company_manager_factory,
    ):
        url = reverse("api:company-manager-list")
        company = company_factory(user=user)
        company_manager_factory.create_batch(3, company=company)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_company_manager(
        self, api_client_auth, user, user_factory, company_factory
    ):
        url = reverse("api:company-manager-list")
        client = api_client_auth(user=user)

        manager = user_factory()
        company = company_factory(user=user)
        data = {"user": str(manager.id), "company": str(company.id)}

        resp = client.post(url, data=data)
        resp_data = resp.json()

        manager.refresh_from_db()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["company"] == str(company.id)
        assert manager.role == user.Roles.MANAGER

    # def test_update_company(self, api_client_auth, user, company_factory):
    #     company = company_factory(user=user)
    #     url = reverse("api:company-detail", args=(company.id,))
    #     data = {"name": "Updated company"}

    #     client = api_client_auth(user=user)
    #     resp = client.patch(url, data=data)
    #     resp_data = resp.json()

    #     assert resp.status_code == status.HTTP_200_OK
    #     assert resp_data["name"] == data["name"]

    def test_read_comapny_manager(self, api_client_auth, user, company_manager_factory):
        company_manger = company_manager_factory(user=user)
        url = reverse("api:company-manager-detail", args=(company_manger.id,))

        client = api_client_auth(user=company_manger.user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["company"]
