from unittest.mock import patch, MagicMock
from django.test import override_settings

from django.core import mail
from django.template.loader import render_to_string

from task_manager.main.models import Task
from task_manager.tasks import send_assign_notification
from tests.base_test_views import TestViewSetBase
from fixtures.factories import UserFactory, TaskFactory


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestSendEmail(TestViewSetBase):
    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = UserFactory.create()
        task = TaskFactory.create(assignee=assignee)

        send_assign_notification.delay(task.id)

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
