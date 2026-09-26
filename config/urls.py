from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Todas as rotas da API ficam sob /api/ (o router do core cuida do resto).
    path("api/", include("core.urls")),
]
