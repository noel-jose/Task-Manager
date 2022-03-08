from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LogoutView


from tasks.views import (
    GenericAllTaskView,
    GenericCompletedTaskView,
    GenericTaskCompleteView,
    GenericTaskCreateView,
    GenericTaskDeleteView,
    GenericTaskDetailView,
    GenericTaskUpdateView,
    GenericTaskView,
    UserCreateView,
    UserLoginView,
    session_storage_view,
    ReminderTimeSetView,
)

from tasks.apiviews import TaskHistoryViewSet, TaskListAPI, TaskViewSet

from rest_framework.routers import SimpleRouter

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("task_manager.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("admin/", admin.site.urls),
    path("tasks/", GenericTaskView.as_view()),
    path("", GenericAllTaskView.as_view()),
    path("create-task/", GenericTaskCreateView.as_view()),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view()),
    path("complete_task/<pk>/", GenericTaskCompleteView.as_view()),
    path("completed_tasks/", GenericCompletedTaskView.as_view()),
    path("all_tasks/", GenericAllTaskView.as_view()),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view()),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view()),
    path("sessiontest", session_storage_view),
    path("user/signup", UserCreateView.as_view()),
    path("user/login", UserLoginView.as_view()),
    path("reminder", ReminderTimeSetView.as_view()),
    path("user/logout", LogoutView.as_view()),
    # path("test_bg", test_bg),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = SimpleRouter()
router.register(prefix="api/tasks", viewset=TaskViewSet)
router.register(prefix="api/history/task", viewset=TaskHistoryViewSet)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
] + router.urls

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
