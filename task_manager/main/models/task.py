from django.db import models

from .user import User


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Task")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    due_at = models.DateTimeField(blank=True, null=True, verbose_name="Due date")
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="task_author"
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="task_executor"
    )

    class State(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    state = models.CharField(
        max_length=255,
        verbose_name="State",
        default=State.NEW_TASK,
        choices=State.choices,
    )

    class Priority(models.TextChoices):
        HIGH = "3"
        MEDIUM = "2"
        LOW = "1"
        NO_PRIORITY = "0"

    priority = models.CharField(
        max_length=255,
        verbose_name="Priority",
        default=Priority.NO_PRIORITY,
        choices=Priority.choices,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-priority"]
