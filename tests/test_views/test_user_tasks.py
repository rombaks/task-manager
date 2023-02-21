from http import HTTPStatus

from tests.base_test_views import TestViewSetBase


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_list(self) -> None:
        user = self.action_client.create_user()
        user_task = self.action_client.create_task(assignee=user["id"])
        self.action_client.create_task()

        tasks = self.list(args=[user["id"]])

        assert tasks == [user_task]

    def test_retrieve_foreign_task(self) -> None:
        user = self.action_client.create_user()
        task = self.action_client.create_task()

        response = self.request_retrieve(args=[user["id"], task["id"]])

        assert response.status_code == HTTPStatus.NOT_FOUND

