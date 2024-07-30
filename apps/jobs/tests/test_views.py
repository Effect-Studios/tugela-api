import pytest
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestTag:
    def test_list_tag(self, api_client_auth, admin, user: User, tag_factory):
        url = reverse("api:tags-list")
        tag_factory.create_batch(3)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_tag(self, api_client_auth, admin):
        url = reverse("api:tags-list")
        client = api_client_auth(user=admin)
        data = {
            "name": "Tag",
        }

        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["name"] == data["name"]

    def test_update_tag(self, api_client_auth, admin, tag_factory):
        tag = tag_factory()
        url = reverse("api:tags-detail", args=(tag.id,))
        data = {"name": "Updated company"}

        client = api_client_auth(user=admin)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["name"] == data["name"]

    def test_read_tag(self, api_client_auth, user, tag_factory):
        tag = tag_factory()
        url = reverse("api:tags-detail", args=(tag.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["name"] == tag.name


class TestJob:
    def test_list_job(
        self, api_client_auth, admin, user: User, job_factory, company_factory
    ):
        url = reverse("api:jobs-list")
        company = company_factory(user=user)
        job_factory.create_batch(3, company=company)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_job(self, api_client_auth, user, company_factory):
        url = reverse("api:jobs-list")
        client = api_client_auth(user=user)
        company = company_factory(user=user)
        data = {
            "title": "Job Title",
            "company": str(company.id),
            "price_type": "per_project",
        }

        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["title"] == data["title"]

    def test_update_job(self, api_client_auth, user, job_factory, company_factory):
        company = company_factory(user=user)
        job = job_factory(company=company)
        data = {"title": "Updated Title"}

        url = reverse("api:jobs-detail", args=(job.id,))
        client = api_client_auth(user=user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["title"] == data["title"]

    def test_read_job(self, api_client_auth, user, job_factory):
        job = job_factory()
        url = reverse("api:jobs-detail", args=(job.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["title"] == job.title


class TestApplication:
    def test_list_application(
        self,
        api_client_auth,
        admin,
        user: User,
        freelancer_factory,
        application_factory,
    ):
        url = reverse("api:applications-list")
        freelancer = freelancer_factory(user=user)
        application_factory.create_batch(3, freelancer=freelancer)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_applications(
        self, api_client_auth, user, job_factory, freelancer_factory
    ):
        url = reverse("api:applications-list")

        freelancer = freelancer_factory(user=user)
        job = job_factory()
        data = {"job": str(job.id), "freelancer": str(freelancer.id)}

        client = api_client_auth(user=user)
        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["status"] == "pending"
        assert resp_data["freelancer"] == str(freelancer.id)
        assert resp_data["job"] == str(job.id)

    def test_update_application(
        self, api_client_auth, user, application_factory, freelancer_factory
    ):
        freelancer = freelancer_factory(user=user)
        application = application_factory(freelancer=freelancer)
        data = {"status": "accepted"}

        url = reverse("api:applications-detail", args=(application.id,))
        client = api_client_auth(user=user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["status"] == data["status"]

    def test_read_application(
        self, api_client_auth, user, application_factory, freelancer_factory
    ):
        freelancer = freelancer_factory(user=user)
        application = application_factory(freelancer=freelancer)
        url = reverse("api:applications-detail", args=(application.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["status"] == application.status
