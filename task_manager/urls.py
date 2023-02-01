"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .main.views import UserViewSet, TaskViewSet, TagViewSet


router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"tags", TagViewSet, basename="tags")

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
