from http import HTTPStatus
import factory
from base import faker

from django.urls import reverse
from rest_framework.test import APITestCase

from task_manager.main.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda _: faker.unique.name())
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class TestJWTAuth(APITestCase):
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")
    any_api_url = "api"

    @staticmethod
    def create_user():
        return UserFactory.create()

    def token_request(self, username: str = None, password: str = "password"):
        client = self.client_class()
        if not username:
            username = self.create_user().username
        return client.post(self.token_url, data={"username": username, "password": password})

    def refresh_token_request(self, refresh_token: str):
        client = self.client_class()
        return client.post(self.refresh_token_url, data={"refresh": refresh_token})

    def get_refresh_token(self):
        response = self.token_request()
        return response.json()["refresh"]

    def test_successful_auth(self):
        response = self.token_request()
        assert response.status_code == HTTPStatus.OK
        assert response.json()["refresh"]
        assert response.json()["access"]
