from django.contrib import admin

from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["id", "nome", "descricao"]
    search_fields = ["nome"]


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["id", "nome", "categoria", "preco", "estoque"]
    list_filter = ["categoria"]
    search_fields = ["nome", "descricao"]
