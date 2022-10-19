import factory
from http import HTTPStatus

from base_test_views import TestViewSetBase
from factories import TaskFactory


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)

    BATCH_SIZE = 3
    tasks_attributes = factory.build_batch(
        dict, FACTORY_CLASS=TaskFactory, size=BATCH_SIZE
    )

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def expected_list(self, entity_list: list[dict], attributes_list: list[dict]):
        expected_list = []
        for index, entity in enumerate(entity_list):
            entity_details = self.expected_details(entity, attributes_list[index])
            expected_list.append(entity_details)
        return expected_list

    def test_create(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        assert task == expected_response

    def test_retrieve(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        retrieved_task = self.retrieve(task["id"])
        assert retrieved_task == expected_response

    def test_list(self):
        tasks = self.create_batch(self.tasks_attributes)
        expected_response = self.expected_list(tasks, self.tasks_attributes)
        task_list =  self.list()
        assert task_list == expected_response

    def test_update(self):
        task = self.create(self.task_attributes)
        new_data = {"title": "Build API 0.1.3"}
        expected_response = self.update(new_data, task["id"])
        updated_task = self.retrieve(task["id"])
        assert updated_task == expected_response

    def test_delete(self):
        task = self.create(self.task_attributes)
        id = self.expected_details(task, self.task_attributes)["id"]
        expected_response = self.delete(id=id)
        assert expected_response.status_code == HTTPStatus.NO_CONTENT
