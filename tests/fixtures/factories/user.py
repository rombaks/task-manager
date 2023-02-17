import factory

from base import faker, ImageFileProvider
from task_manager.main.models import User

factory.Faker.add_provider(ImageFileProvider)


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
    avatar_picture = factory.Faker("image_file", fmt="jpeg")
