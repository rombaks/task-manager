import factory
from http import HTTPStatus
import json

from base_test_views import TestViewSetBase
from factories import TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    BATCH_SIZE = 3
    tags_attributes = factory.build_batch(
        dict, FACTORY_CLASS=TagFactory, size=BATCH_SIZE
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
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_retrieve(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        retrieved_tag = self.retrieve(tag["id"])
        assert retrieved_tag == expected_response

    def test_list(self):
        tags = self.create_batch(self.tags_attributes)
        expected_response = self.expected_list(tags, self.tags_attributes)
        tag_list = self.list()
        assert tag_list == expected_response

    def test_update(self):
        tag = self.create(self.tag_attributes)
        new_data = {"title": "backup"}
        expected_response = self.update(new_data, tag["id"])
        updated_tag = self.retrieve(tag["id"])
        assert updated_tag == expected_response

    def test_delete(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.delete(tag["id"])
        assert expected_response.status_code == HTTPStatus.NO_CONTENT

    def test_not_found(self):
        expected_response = self.client.get("/not_found")
        assert expected_response.status_code == HTTPStatus.NOT_FOUND

    def test_anonymous_create(self):
        response = self.anonymous_create(self.tag_attributes)
        expected_error = "Authentication credentials were not provided."
        assert response["detail"] == expected_error
