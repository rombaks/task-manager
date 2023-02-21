from collections import namedtuple
from http import HTTPStatus
from typing import List, Optional, Union

import factory
from django.urls import reverse
from rest_framework.test import APIClient
from task_manager.main.models import User
from tests.fixtures.factories import TaskFactory, UserFactory, TagFactory

ModelSetup = namedtuple("ModelSetup", "basename factory_class")


class ActionClient:
    USER_SETUP = ModelSetup("users", UserFactory)
    TASK_SETUP = ModelSetup("tasks", TaskFactory)
    TAG_SETUP = ModelSetup("tags", TagFactory)

    def __init__(self, client: APIClient) -> None:
        self.client = client
        self.user: Optional[User] = None

    def init_user(self) -> None:
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)  # type: ignore

    def detail_url(self, basename, key: Union[int, str]) -> str:
        return reverse(f"{basename}-detail", args=[key])

    def list_url(self, basename, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{basename}-list", args=args)

    def request_create(self, model_setup: namedtuple, **attributes):
        basename = model_setup.basename
        factory_class = model_setup.factory_class

        mock_attributes = factory.build(dict, FACTORY_CLASS=factory_class)
        mock_attributes.update(attributes)

        response = self.client.post(self.list_url(basename=basename), mock_attributes)
        return response

    def create(self, model_setup: namedtuple, **attributes):
        response = self.request_create(model_setup, **attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def create_user(self, **attributes):
        user = self.create(model_setup=self.USER_SETUP, **attributes)
        return user

    def create_task(self, **attributes) -> dict:
        task = self.create(model_setup=self.TASK_SETUP, **attributes)
        return task

    def create_tag(self, **attributes) -> dict:
        task = self.create(model_setup=self.TAG_SETUP, **attributes)
        return task
