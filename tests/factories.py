import factory

from base import faker
from task_manager.main.models import User, Task, Tag


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.unique.word())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    date_of_birth = factory.LazyAttribute(
        lambda _: faker.date_of_birth().strftime("%Y-%m-%d")
    )
    phone = factory.LazyAttribute(lambda _: faker.unique.phone_number())


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.LazyAttribute(lambda _: faker.unique.word())


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=10))
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=50))

    author = None
    assignee = None

    created_at = factory.LazyAttribute(
        lambda _: faker.past_datetime().strftime("%Y-%m-%dT%XZ")
    )
    updated_at = factory.LazyAttribute(
        lambda _: faker.past_datetime().strftime("%Y-%m-%dT%XZ")
    )
    due_at = factory.LazyAttribute(
        lambda _: faker.future_datetime().strftime("%Y-%m-%dT%XZ")
    )

    state = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "new",
                "in_development",
                "in_qa",
                "in_code_review",
                "ready_for_release",
                "released",
                "archived",
            ]
        )
    )

    priority = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "0",
                "1",
                "2",
                "3",
            ]
        )
    )
