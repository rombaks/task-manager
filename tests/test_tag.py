import factory
from http import HTTPStatus

from base_test_views import TestViewSetBase
from factories import TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.tag_attributes
        assert tag == expected_response
