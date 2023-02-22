from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .main.views import (
    TaskTagsViewSet,
    UserViewSet,
    TaskViewSet,
    TagViewSet,
    CurrentUserViewSet,
    UserTasksViewSet,
)
from .main.services.single_resource import BulkRouter


router = BulkRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"current-user", CurrentUserViewSet, basename="current_user")

users = router.register(r"users", UserViewSet, basename="users")
users.register(
    r"tasks",
    UserTasksViewSet,
    basename="user_tasks",
    parents_query_lookups=["assignee_id"],
)

tasks = router.register(r"tasks", TaskViewSet, basename="tasks")
tasks.register(
    r"tags",
    TaskTagsViewSet,
    basename="task_tags",
    parents_query_lookups=["task_id"],
)

schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version="v1",
        description="Project helps you to get things done!",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rombaks.dev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

admin.site.site_header = "Task Manager"
admin.site.site_title = "DBL"
admin.site.index_title = "Task Manager"

urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage/homepage.html")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
