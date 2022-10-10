from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tag, Task


class CustomUserAdmin(UserAdmin):
    model = User
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                )
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "username",
                        "email",
                        "first_name",
                        "last_name",
                        "is_staff",
                    )
                ),
            },
        ),
    )

    list_display = ("first_name", "last_name", "email", "role")
    list_filter = ("role",)
    ordering = ("email",)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "assignee",
        "due_at",
        "state",
        "priority",
    )
    list_display_links = ("title",)
    search_fields = ("title",)

    list_editable = ("state",)
    list_filter = ("state", "priority")


class TagAdmin(admin.ModelAdmin):
    list_display = ("title", )
    list_display_links = ("title", )
    search_fields = ("title", )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
