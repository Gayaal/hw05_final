from about.apps import AboutConfig

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from posts.apps import PostsConfig

from users.apps import UsersConfig

urlpatterns = [
    path("", include("posts.urls", namespace=PostsConfig.name)),
    path("about/", include("about.urls", namespace=AboutConfig.name)),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls", namespace=UsersConfig.name)),
    path("auth/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"
handler403 = "core.views.csrf_failure"
