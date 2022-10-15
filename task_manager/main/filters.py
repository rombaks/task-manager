import django_filters

from .models import User, Task


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "last_name": ["icontains"],
        }


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            "tag__title": ["iexact"]
        }
