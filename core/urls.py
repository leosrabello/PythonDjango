"""Rotas do app core.

O DefaultRouter gera as URLs de CRUD automaticamente para cada ViewSet
registrado:

    /api/categorias/       GET (lista) · POST (cria)
    /api/categorias/{id}/  GET · PUT · PATCH · DELETE

    Frente 3 (Produto):
        from .views import ProdutoViewSet
        router.register("produtos", ProdutoViewSet)
"""

from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet)

# As frentes registram os ViewSets acima desta linha.

urlpatterns = router.urls
