from django.db import models
from django.utils import timezone

from .user import User
from .tag import Tag


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Task")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Updated at")
    due_at = models.DateTimeField(blank=True, null=True, verbose_name="Due date")
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="task_author",
        blank=True,
        null=True,
        verbose_name="author",
    )

    assignee = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="Task_assignee"
    )
    tags = models.ManyToManyField(
        Tag, related_name="Tag", verbose_name="Tag", blank=True
    )

    class State(models.TextChoices):
        NEW = "new"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    state = models.CharField(
        max_length=255,
        verbose_name="State",
        default=State.NEW,
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
