from rest_framework import viewsets
import django_filters

from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ('name',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskFilter(django_filters.FilterSet):

    tag__title = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Task
        fields = (
            "state",
            "tag__title",
            "author__username",
            "assignee__username",
        )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("author", "assignee").order_by("priority")
    serializer_class = TaskSerializer
    filter_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("title")
    serializer_class = TagSerializer
