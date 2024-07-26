import pytest
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from rest_framework import status

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestFreelancer:
    def test_list_freelancer(
        self, api_client_auth, admin, user: User, freelancer_factory
    ):
        url = reverse("api:freelancers-list")
        freelancer_factory.create_batch(
            3,
        )

        client = api_client_auth(user=admin)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_freelancer(self, api_client_auth, user):
        url = reverse("api:freelancers-list")
        client = api_client_auth(user=user)
        data = {
            "user": str(user.id),
        }

        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["user"] == data["user"]

    def test_update_freelancer(self, api_client_auth, user, freelancer_factory):
        freelancer = freelancer_factory(user=user)
        url = reverse("api:freelancers-detail", args=(freelancer.id,))
        data = {"how_you_found_us": "twitter"}

        client = api_client_auth(user=user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["how_you_found_us"] == data["how_you_found_us"]

    def test_read_freelancer(self, api_client_auth, user, freelancer_factory):
        freelancer = freelancer_factory(user=user)
        url = reverse("api:freelancers-detail", args=(freelancer.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["how_you_found_us"] == freelancer.how_you_found_us


class TestWorkExpperience:
    def test_list_experiences(
        self, api_client_auth, user: User, freelancer_factory, work_experience_factory
    ):
        url = reverse("api:work-experiences-list")
        freelancer = freelancer_factory(user=user)
        work_experience_factory.create_batch(3, freelancer=freelancer, user=user)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_experience(self, api_client_auth, user, freelancer_factory):
        url = reverse("api:work-experiences-list")
        freelancer = freelancer_factory(user=user)
        client = api_client_auth(user=user)
        data = {
            "freelancer": str(freelancer.id),
            "job_title": "Job Title",
            "company_name": "Company Name",
            "start_date": "2019-08-24",
        }

        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["freelancer"] == data["freelancer"]
        assert resp_data["currently_working_here"] is False

    def test_update_experiences(
        self, api_client_auth, user, freelancer_factory, work_experience_factory
    ):
        freelancer = freelancer_factory(user=user)
        work_experience = work_experience_factory.create(
            user=user, freelancer=freelancer
        )
        url = reverse("api:work-experiences-detail", args=(work_experience.id,))
        data = {"job_title": "Updated Title"}

        client = api_client_auth(user=user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["job_title"] == data["job_title"]

    def test_read_experiences(
        self, api_client_auth, user, freelancer_factory, work_experience_factory
    ):
        freelancer = freelancer_factory(user=user)
        work_experience = work_experience_factory.create(
            user=user, freelancer=freelancer
        )
        url = reverse("api:work-experiences-detail", args=(work_experience.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["company_name"] == work_experience.company_name


class TestPortfolioItem:
    def test_list_portfolio(
        self, api_client_auth, user: User, portfolio_item_factory, freelancer_factory
    ):
        url = reverse("api:portfolio-items-list")
        freelancer = freelancer_factory(user=user)
        portfolio_item_factory.create_batch(3, freelancer=freelancer)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_portfolio(self, api_client_auth, user: User, freelancer_factory):
        url = reverse("api:portfolio-items-list")
        freelancer = freelancer_factory(user=user)
        client = api_client_auth(user=user)

        data = {
            "freelancer": str(freelancer.id),
            "title": "Title",
            "start_date": "2019-08-24",
        }

        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["freelancer"] == data["freelancer"]
        assert resp_data["start_date"] == data["start_date"]
        assert resp_data["title"] == data["title"]

    def test_update_portfolio(
        self, api_client_auth, user, freelancer_factory, portfolio_item_factory
    ):
        freelancer = freelancer_factory(user=user)
        portfolio = portfolio_item_factory.create(user=user, freelancer=freelancer)
        url = reverse("api:portfolio-items-detail", args=(portfolio.id,))
        data = {"title": "Updated Title"}

        client = api_client_auth(user=user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["title"] == data["title"]

    def test_read_portfolio(
        self, api_client_auth, user, freelancer_factory, portfolio_item_factory
    ):
        freelancer = freelancer_factory(user=user)
        portfolio = portfolio_item_factory.create(user=user, freelancer=freelancer)
        url = reverse("api:portfolio-items-detail", args=(portfolio.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["title"] == portfolio.title


class TestService:
    def test_list_service(
        self, api_client_auth, user: User, service_factory, freelancer_factory
    ):
        url = reverse("api:services-list")
        freelancer = freelancer_factory(user=user)
        service_factory.create_batch(3, freelancer=freelancer)

        client = api_client_auth(user=user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data["results"]) == 3

    def test_create_service(self, api_client_auth, user: User, freelancer_factory):
        url = reverse("api:services-list")
        freelancer = freelancer_factory(user=user)
        client = api_client_auth(user=user)

        data = {
            "freelancer": str(freelancer.id),
            "title": "Title",
            "price_type": "per_project",
        }

        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["freelancer"] == data["freelancer"]
        assert resp_data["price_type"] == data["price_type"]
        assert resp_data["title"] == data["title"]

    def test_update_service(
        self, api_client_auth, user, freelancer_factory, service_factory
    ):
        freelancer = freelancer_factory(user=user)
        service = service_factory.create(user=user, freelancer=freelancer)
        url = reverse("api:services-detail", args=(service.id,))
        data = {"title": "Updated Title"}

        client = api_client_auth(user=user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["title"] == data["title"]

    def test_read_service(
        self, api_client_auth, user, freelancer_factory, service_factory
    ):
        freelancer = freelancer_factory(user=user)
        service = service_factory.create(user=user, freelancer=freelancer)
        url = reverse("api:services-detail", args=(service.id,))

        client = api_client_auth(user=user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["title"] == service.title
