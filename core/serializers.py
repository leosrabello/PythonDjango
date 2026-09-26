# Serializers (ModelSerializer): validam o payload de entrada e transformam
# os objetos em JSON na saída. É o equivalente à validação + formatação.
#
# Frente 2 (Categoria):
#     class CategoriaSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Categoria
#             fields = ["id", "nome", "descricao"]
#
# Frente 3 (Produto) com serializer ANINHADO (mostra a categoria dentro do produto):
#     class ProdutoSerializer(serializers.ModelSerializer):
#         categoria = CategoriaSerializer(read_only=True)          # leitura: aninhado
#         categoria_id = serializers.PrimaryKeyRelatedField(       # escrita: só o id
#             queryset=Categoria.objects.all(), source="categoria", write_only=True)
#         class Meta:
#             model = Produto
#             fields = ["id", "nome", "descricao", "preco", "estoque",
#                       "categoria", "categoria_id"]
