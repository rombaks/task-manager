import factory
from http import HTTPStatus

from base_test_views import TestViewSetBase
from factories import TaskFactory


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        assert task == expected_response

    def test_retrieve(self):
        task = self.create(self.task_attributes)
        id = self.expected_details(task, self.task_attributes)["id"]
        expected_response = self.retrieve(id=id)
        assert task == expected_response

    def test_update(self):
        task = self.create(self.task_attributes)
        id = self.expected_details(task, self.task_attributes)["id"]
        new_data = {"title": "Build API 0.1.3"}
        expected_response = self.update(data=new_data, id=id)
        updated_task = self.retrieve(id=id)
        assert updated_task == expected_response

    def test_delete(self):
        task = self.create(self.task_attributes)
        id = self.expected_details(task, self.task_attributes)["id"]
        expected_response = self.delete(id=id)
        assert expected_response.status_code == HTTPStatus.NO_CONTENT
