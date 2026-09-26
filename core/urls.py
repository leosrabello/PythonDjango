"""Rotas do app core.

O DefaultRouter gera as URLs de CRUD automaticamente para cada ViewSet
registrado:

    /api/categorias/       GET (lista) · POST (cria)
    /api/categorias/{id}/  GET · PUT · PATCH · DELETE

    /api/produtos/        GET (lista) · POST (cria)
    /api/produtos/{id}/   GET · PUT · PATCH · DELETE
"""

from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, ProdutoViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet)
router.register("produtos", ProdutoViewSet)

# As frentes registram os ViewSets acima desta linha.

urlpatterns = router.urls
