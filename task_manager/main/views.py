from rest_framework import viewsets


from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .filters import UserFilter, TaskFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("author", "assignee").order_by("id")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
