from http import HTTPStatus
import factory
from task_manager.main.models import Task
from tests.base_test_views import TestViewSetBase
from tests.fixtures.factories.tag import TagFactory


class TestTaskTagsViewSet(TestViewSetBase):
    basename = "task_tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {"id": entity["id"], **attributes}

    def test_list(self) -> None:
        task = self.action_client.create_task()
        tag1 = self.action_client.create_tag()
        tag2 = self.action_client.create_tag()
        self.add_tags(task, [tag1, tag2])

        tags = self.list(args=[task["id"]])

        assert tags == [tag1, tag2]

    def test_retrieve(self) -> None:
        task = self.action_client.create_task()
        expected_tag = self.action_client.create_tag()
        self.add_tags(task, [expected_tag])

        tag = self.retrieve(args=[task["id"], expected_tag["id"]])

        assert tag == expected_tag

    def test_create(self):
        task = self.action_client.create_task()
        tag1 = self.action_client.create_tag()
        tag2 = self.action_client.create_tag()
        self.add_tags(task, [tag1, tag2])

        tag = self.create(data=self.tag_attributes, args=[task["id"]])

        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_update(self):
        task = self.action_client.create_task()
        tag1 = self.action_client.create_tag()
        tag2 = self.action_client.create_tag()
        self.add_tags(task, [tag1, tag2])

        tag = self.bulk_update(data=self.tag_attributes, args=[task["id"]])

        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_delete(self) -> None:
        task = self.action_client.create_task()
        expected_tag = self.action_client.create_tag()
        self.add_tags(task, [expected_tag])

        response = self.delete(args=[task["id"], expected_tag["id"]])

        assert response.status_code == HTTPStatus.NO_CONTENT

    def add_tags(self, task: dict, tags: list) -> None:
        task_instance = Task.objects.get(pk=task["id"])
        task_instance.tags.add(*self.ids(tags))
        task_instance.save()
