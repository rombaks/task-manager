import factory

from tests.base import faker
from task_manager.main.models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=10))
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=50))

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

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.groups.add(*extracted)
