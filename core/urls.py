"""Rotas do app core.

O DefaultRouter gera as URLs de CRUD automaticamente para cada ViewSet
registrado. Cada frente registra o seu aqui:

    Frente 2 (Categoria):
        from .views import CategoriaViewSet
        router.register("categorias", CategoriaViewSet)

    Frente 3 (Produto):
        from .views import ProdutoViewSet
        router.register("produtos", ProdutoViewSet)

Enquanto nada está registrado, o router só expõe a raiz da API (/api/),
que já serve para confirmar que o projeto está de pé.
"""

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# As frentes registram os ViewSets acima desta linha.

urlpatterns = router.urls
