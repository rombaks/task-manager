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
