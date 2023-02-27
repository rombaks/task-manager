from http import HTTPStatus
from typing import List, Optional, Union

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from task_manager.main.models import User
from tests.fixtures.action_client import ActionClient


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    action_client: Optional[ActionClient] = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = APIClient()
        cls.action_client = ActionClient(cls.client)
        cls.action_client.init_user()
        cls.user = cls.action_client.user

    @classmethod
    def detail_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-detail", args=args)

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data)
        return response

    def request_retrieve(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(args))
        return response

    def request_list(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args))
        return response

    def request_update(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.patch(self.detail_url(args), data=data)
        return response

    def request_delete(self, args: List[Union[str, int]]) -> dict:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(args))
        return response

    def create_batch(self, batch_attributes: list[dict]) -> list[dict]:
        batch = [self.create(data) for data in batch_attributes]
        return batch

    def retrieve(self, args: List[Union[str, int]] = None) -> dict:
        response = self.request_retrieve(args=args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def list(self, args: List[Union[str, int]] = None) -> dict:
        response = self.request_list(args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, args: List[Union[str, int]]) -> dict:
        response = self.request_update(data, args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, args: List[Union[str, int]]) -> dict:
        response = self.request_delete(args)
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response

    def anonymous_create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.logout()
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.FORBIDDEN
        return response.data

    def request_single_resource(self, data: dict = None) -> Response:
        self.client.force_login(self.user)
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, data: dict) -> Response:
        self.client.force_login(self.user)
        url = self.list_url()
        return self.client.patch(url, data=data)

    def patch_single_resource(self, data: dict) -> dict:
        response = self.request_patch_single_resource(data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_bulk_update(
        self, data: dict, args: List[Union[str, int]] = None
    ) -> Response:
        self.client.force_login(self.user)
        url = self.list_url(args)
        return self.client.put(url, data=data)

    def bulk_update(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.request_bulk_update(data, args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def ids(self, entities: List[dict] = None) -> List[Optional[int]]:
        return [entity.get("id") for entity in entities]
