from django.db import models

# As entidades (tabelas) do domínio ficam aqui. Tema: loja de eletrônicos.


class Categoria(models.Model):
    """Categoria de produtos (ex.: Notebooks, Smartphones).

    Lado "1" do relacionamento 1:N — uma categoria tem vários produtos.
    """

    nome = models.CharField(max_length=80, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """Produto pertencente a uma categoria da loja."""

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="produtos",
    )
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)

    class Meta:
        ordering = ["nome"]
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    def __str__(self):
        return self.nome
