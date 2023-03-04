from rest_framework import serializers
from django.core.files.base import File
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from .models import tag, user, task
from task_manager.settings import UPLOAD_MAX_SIZES


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = user.User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
            "avatar_picture",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = tag.Tag
        fields = (
            "id",
            "title",
        )


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = task.Task
        fields = (
            "id",
            "title",
            "description",
            "author",
            "assignee",
            "due_at",
            "created_at",
            "updated_at",
            "state",
            "priority",
            "tags",
        )
