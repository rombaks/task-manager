import factory
from http import HTTPStatus

from base_test_views import TestViewSetBase
from factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    BATCH_SIZE = 5
    users_attribures = factory.build_batch(
        dict, FACTORY_CLASS=UserFactory, size=BATCH_SIZE
    )

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_retrieve(self):
        user = self.create(self.user_attributes)
        id = self.expected_details(user, self.user_attributes)["id"]
        expected_response = self.retrieve(id=id)
        assert user == expected_response

    def test_update(self):
        user = self.create(self.user_attributes)
        id = self.expected_details(user, self.user_attributes)["id"]
        new_data = {"last_name": "Smith"}
        expected_response = self.update(data=new_data, id=id)
        updated_user = self.retrieve(id=id)
        assert updated_user == expected_response

    def test_delete(self):
        user = self.create(self.user_attributes)
        id = self.expected_details(user, self.user_attributes)["id"]
        expected_response = self.delete(id=id)
        assert expected_response.status_code == HTTPStatus.NO_CONTENT

    def test_not_found(self):
        expected_response = self.client.get("/not_found")
        assert expected_response.status_code == HTTPStatus.NOT_FOUND
