# Serializers (ModelSerializer): validam o payload de entrada e transformam
# os objetos em JSON na saída. É o equivalente à validação + formatação.

from rest_framework import serializers

from .models import Categoria, Produto


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


class ProdutoSerializer(serializers.ModelSerializer):
    """Exibe a categoria completa e recebe seu ID nas operações de escrita."""

    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source="categoria",
        write_only=True,
    )

    class Meta:
        model = Produto
        fields = [
            "id",
            "nome",
            "descricao",
            "preco",
            "estoque",
            "categoria",
            "categoria_id",
        ]

    def validate_nome(self, value):
        nome = value.strip()
        if not nome:
            raise serializers.ValidationError("O nome não pode ficar em branco.")
        return nome

    def validate_preco(self, value):
        if value < 0:
            raise serializers.ValidationError("O preço não pode ser negativo.")
        return value

    def validate_estoque(self, value):
        if value < 0:
            raise serializers.ValidationError("O estoque não pode ser negativo.")
        return value
