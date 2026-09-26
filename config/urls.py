from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/api/", permanent=False), name="home"),
    # Todas as rotas da API ficam sob /api/ (o router do core cuida do resto).
    path("api/", include("core.urls")),
]
