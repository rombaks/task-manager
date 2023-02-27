from http import HTTPStatus

from typing import TYPE_CHECKING, Any

from django.forms.models import model_to_dict
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from task_manager.main.models import Tag, Task


if TYPE_CHECKING:
    BaseViewMixinBaseClass = viewsets.GenericViewSet
else:
    BaseViewMixinBaseClass = object


class TaskTagsViewMixin(BaseViewMixinBaseClass):
    """
    create: Get or create new tag and add it to task tag list
    bulk_update: Replace task current tags by new one
    delete: Delete tag by id from task tag list
    """

    def create(self, request: Request, *_: Any, **___: Any) -> Response:
        """Get or create new tag and add it to task tag list"""
        task = self._get_task()
        tag, data = self._get_or_create_valid_tag(request=request)

        task.tags.add(tag)

        return Response(data=data, status=HTTPStatus.CREATED)
