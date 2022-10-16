import factory
from http import HTTPStatus

from base_test_views import TestViewSetBase
from factories import TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_retrieve(self):
        tag = self.create(self.tag_attributes)
        id = self.expected_details(tag, self.tag_attributes)["id"]
        expected_response = self.retrieve(id=id)
        assert tag == expected_response

    def test_update(self):
        tag = self.create(self.tag_attributes)
        id = self.expected_details(tag, self.tag_attributes)["id"]
        new_data = {"title": "backup"}
        expected_response = self.update(data=new_data, id=id)
        updated_tag = self.retrieve(id=id)
        assert updated_tag == expected_response

    def test_delete(self):
        tag = self.create(self.tag_attributes)
        id = self.expected_details(tag, self.tag_attributes)["id"]
        expected_response = self.delete(id=id)
        assert expected_response.status_code == HTTPStatus.NO_CONTENT

    def test_not_found(self):
        expected_response = self.client.get("/not_found")
        assert expected_response.status_code == HTTPStatus.NOT_FOUND
