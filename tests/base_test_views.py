import factory

from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from task_manager.main.models import User, Task
from factories import UserFactory, TaskFactory


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    @staticmethod
    def create_api_user():
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        return User.objects.create(**user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def retrieve(self, id: int = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(id))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, id: int = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.patch(self.detail_url(id), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, id: int = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(id))
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response

    def anonymous_create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.logout()
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.FORBIDDEN
        return response
