# Serializers (ModelSerializer): validam o payload de entrada e transformam
# os objetos em JSON na saída. É o equivalente à validação + formatação.

from rest_framework import serializers

from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    """Converte Categoria <-> JSON e valida o que chega no POST/PUT/PATCH."""

    class Meta:
        model = Categoria
        fields = ["id", "nome", "descricao"]

    def validate_nome(self, value):
        """Nome não pode ser só espaço em branco; guarda o valor já limpo."""
        nome = value.strip()
        if not nome:
            raise serializers.ValidationError("O nome não pode ficar em branco.")
        return nome


# Frente 3 (Produto) com serializer ANINHADO (mostra a categoria dentro do produto):
#     class ProdutoSerializer(serializers.ModelSerializer):
#         categoria = CategoriaSerializer(read_only=True)          # leitura: aninhado
#         categoria_id = serializers.PrimaryKeyRelatedField(       # escrita: só o id
#             queryset=Categoria.objects.all(), source="categoria", write_only=True)
#         class Meta:
#             model = Produto
#             fields = ["id", "nome", "descricao", "preco", "estoque",
#                       "categoria", "categoria_id"]
