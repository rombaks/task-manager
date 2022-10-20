import factory
from http import HTTPStatus

from base_test_views import TestViewSetBase
from factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    BATCH_SIZE = 3
    users_attributes = factory.build_batch(
        dict, FACTORY_CLASS=UserFactory, size=BATCH_SIZE
    )

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def expected_list(self, entity_list: list[dict], attributes_list: list[dict]):
        authtorized_user = self.retrieve(self.user.id)
        expected_list = [authtorized_user]

        for index, entity in enumerate(entity_list):
            entity_details = self.expected_details(entity, attributes_list[index])
            expected_list.append(entity_details)
        return expected_list

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_retrieve(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        retrieved_user = self.retrieve(user["id"])
        assert retrieved_user == expected_response

    def test_list(self):
        users = self.create_batch(self.users_attributes)
        expected_response = self.expected_list(users, self.users_attributes)
        user_list = self.list()
        assert user_list == expected_response

    def test_update(self):
        user = self.create(self.user_attributes)
        new_data = {"last_name": "Smith"}
        updated_attributes = dict(self.tag_attributes, **new_data)
        expected_response =  self.expected_details(tag, updated_attributes)
        response = self.update(new_data, user["id"])
        assert response == expected_response

    def test_delete(self):
        user = self.create(self.user_attributes)
        response = self.delete(user["id"])
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_not_found(self):
        response = self.client.get("/not_found")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_anonymous_create(self):
        response = self.anonymous_create(self.user_attributes)
        expected_error = "Authentication credentials were not provided."
        assert response["detail"] == expected_error
