from typing import cast
from rest_framework import viewsets
from .services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin
from .services.nested_resource import TaskTagsViewMixin


from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .filters import UserFilter, TaskFilter
from rest_framework_extensions.mixins import NestedViewSetMixin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "assignee")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("author", "assignee").order_by("id")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TaskTagsViewSet(TaskTagsViewMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
