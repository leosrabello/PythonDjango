# As views expõem o CRUD. Opção escolhida: ModelViewSet (o DRF gera os 6
# verbos automaticamente e o DefaultRouter cria as URLs).

from rest_framework import viewsets

from .models import Categoria
from .serializers import CategoriaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """CRUD completo de /api/categorias/.

    GET lista (200) · GET id (200/404) · POST (201/400)
    PUT/PATCH (200/400/404) · DELETE (204/404)
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


# Frente 3 (Produto):
#     class ProdutoViewSet(viewsets.ModelViewSet):
#         queryset = Produto.objects.select_related("categoria").all()
#         serializer_class = ProdutoSerializer
#
# Depois, registre o ViewSet no core/urls.py (router.register(...)).
