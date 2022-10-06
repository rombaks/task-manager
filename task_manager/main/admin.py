from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tag, Task

admin.site.register(User, UserAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "executor",
        "due_at",
        "created_at",
        "updated_at",
        "state",
        "priority",
    )
    list_display_links = ("title",)
    search_fields = ("title",)

    list_editable = ("state",)
    list_filter = ("state", "priority")


class TagAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_display_links = ["title"]
    search_fields = ["title"]


admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
