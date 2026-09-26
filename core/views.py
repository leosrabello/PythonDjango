# As views expõem o CRUD. Opção escolhida: ModelViewSet (o DRF gera os 6
# verbos automaticamente e o DefaultRouter cria as URLs).

from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError

from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """CRUD completo de /api/categorias/.

    GET lista (200) · GET id (200/404) · POST (201/400)
    PUT/PATCH (200/400/404) · DELETE (204/404)
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    """CRUD de produtos, com busca textual, filtro por categoria e ordenação."""

    queryset = Produto.objects.select_related("categoria").all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome", "descricao", "categoria__nome"]
    ordering_fields = ["nome", "preco", "estoque"]
    ordering = ["nome"]

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.query_params.get("categoria")

        if categoria_id:
            try:
                categoria_id = int(categoria_id)
            except (TypeError, ValueError):
                raise ValidationError(
                    {"categoria": "Informe um ID de categoria válido."}
                )

            if categoria_id < 1:
                raise ValidationError(
                    {"categoria": "Informe um ID de categoria válido."}
                )

            queryset = queryset.filter(categoria_id=categoria_id)

        return queryset
