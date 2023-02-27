from task_manager.main.models import Task
from tests.base_test_views import TestViewSetBase


class TestTaskTagsViewSet(TestViewSetBase):
    basename = "task_tags"

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
    def add_tags(self, task: dict, tags: list) -> None:
        task_instance = Task.objects.get(pk=task["id"])
        task_instance.tags.add(*self.ids(tags))
        task_instance.save()
