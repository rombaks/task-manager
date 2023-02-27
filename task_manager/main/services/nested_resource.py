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

    def bulk_update(self, request: Request, *__: Any, **___: Any) -> Response:
        """Replace task current tags by new one"""
        tag, data = self._get_or_create_valid_tag(request=request)
        task = self._get_task()

        task.tags.clear()
        task.tags.add(tag)

        return Response(data=data, status=HTTPStatus.OK)

    def destroy(self, _: Request, *__: Any, **___: Any) -> Response:
        """Delete tag by id from task tag list"""
        tag = self.get_object()
        task = self._get_task()

        task.tags.remove(tag)

        return Response(status=HTTPStatus.NO_CONTENT)

    def _get_or_create_valid_tag(self, request: Request) -> tuple[Tag, dict]:
        try:
            tag = Tag.objects.get(**request.data)
            data = model_to_dict(tag)
        except Tag.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            tag = serializer.save()
            data = serializer.data

        return tag, data

    def _get_task(self) -> Task:
        task_id = self.kwargs["parent_lookup_task_id"]
        task = Task.objects.get(pk=task_id)

        return task
