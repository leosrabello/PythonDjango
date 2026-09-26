# As views expõem o CRUD. Opção recomendada: ModelViewSet (o DRF gera os 6
# verbos automaticamente e o DefaultRouter cria as URLs).
#
# Frente 2 (Categoria):
#     class CategoriaViewSet(viewsets.ModelViewSet):
#         queryset = Categoria.objects.all().order_by("nome")
#         serializer_class = CategoriaSerializer
#
# Frente 3 (Produto):
#     class ProdutoViewSet(viewsets.ModelViewSet):
#         queryset = Produto.objects.select_related("categoria").all()
#         serializer_class = ProdutoSerializer
#
# Depois, registre o ViewSet no core/urls.py (router.register(...)).
